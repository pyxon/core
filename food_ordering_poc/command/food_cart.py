import inspect
import logging
from collections import defaultdict
from typing import MutableMapping
from uuid import UUID

from pyxon.core.command_handling.registry import AggregateCommandHandler
from pyxon.core.command_handling.registry import CommandHandlingRegistry
from pyxon.core.modelling.command import AggregateLifecycle
from food_ordering_poc.shared.commands import ConfirmOrderCommand
from food_ordering_poc.shared.commands import CreateFoodCartCommand
from food_ordering_poc.shared.commands import DeselectProductCommand
from food_ordering_poc.shared.commands import SelectProductCommand
from food_ordering_poc.shared.events import FoodCartCreatedEvent
from food_ordering_poc.shared.events import OrderConfirmedEvent
from food_ordering_poc.shared.events import ProductDeselectedEvent
from food_ordering_poc.shared.events import ProductSelectedEvent
from food_ordering_poc.shared.exceptions import ProductDeselectionException


def log(o):
    return logging.getLogger(o.__class__.__name__)


def aggregate(identifier: str):
    def wrapper(cls):
        print(f"%%% {cls.__name__} identifier is {identifier}")
        for func_name in dir(cls):
            func = getattr(cls, func_name)
            if callable(func) and hasattr(func, "__handle_command__"):
                CommandHandlingRegistry.register_command_handler(
                    AggregateCommandHandler(cls, func),
                )
        return cls
    return wrapper


def command_handler(func):
    annotations = inspect.getfullargspec(func).annotations
    command_arg_name = next(
        (
            arg_name
            for arg_name, arg_value in annotations.items()
            if arg_name == "command"  # TODO: Analyze arg_value instead of arg_name
        ),
        None,
    )
    if command_arg_name is None:
        raise Exception("command argument not found in command handler")
    func.__handle_command__ = annotations[command_arg_name]
    return func


@aggregate(identifier="_food_cart_id")
class FoodCart:

    _food_cart_id: UUID
    _selected_products: MutableMapping[UUID, int]
    _confirmed: bool

    @command_handler
    def __init__(self, command: CreateFoodCartCommand):
        log(self).info("CreateFoodCartCommand handler")
        AggregateLifecycle.apply(FoodCartCreatedEvent(command.food_cart_id))

    @command_handler
    def handle_select_product(self, command: SelectProductCommand):
        log(self).info("SelectProductCommand handler")
        AggregateLifecycle.apply(ProductSelectedEvent(self._food_cart_id, command.product_id, command.quantity))

    @command_handler
    def handle_deselect_product(self, command: DeselectProductCommand):
        log(self).info("DeselectProductCommand handler")
        product_id = command.product_id
        quantity = command.quantity

        if product_id not in self._selected_products:
            raise ProductDeselectionException(
                "Cannot deselect a product which has not been selected for this Food Cart",
            )
        if self._selected_products[product_id] - quantity < 0:
            raise ProductDeselectionException(
                f"Cannot deselect more products of ID {product_id} than have been selected initially",
            )

        AggregateLifecycle.apply(ProductDeselectedEvent(self._food_cart_id, command.product_id, command.quantity))

    @command_handler
    def handle_confirm_order(self, command: ConfirmOrderCommand):
        log(self).info("ConfirmOrderCommand handler")
        if self._confirmed:
            log(self).warning("Cannot confirm a Food Cart order which is already confirmed")
            return

        AggregateLifecycle.apply(OrderConfirmedEvent(self._food_cart_id))

    # @EventSourcingHandler
    def on_food_cart_created(self, event: FoodCartCreatedEvent):
        self._food_cart_id = event.food_cart_id
        self._selected_products = defaultdict(int)
        self._confirmed = False

    # @EventSourcingHandler
    def on_product_selected(self, event: ProductSelectedEvent):
        self._selected_products[event.product_id] += event.quantity

    # @EventSourcingHandler
    def on_product_deselected(self, event: ProductDeselectedEvent):
        self._selected_products[event.product_id] -= event.quantity

    # @EventSourcingHandler
    def on_order_confirmed(self, event: OrderConfirmedEvent):
        self._confirmed = True
