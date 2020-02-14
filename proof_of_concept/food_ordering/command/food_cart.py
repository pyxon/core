import logging
from collections import defaultdict
from typing import MutableMapping
from uuid import UUID
from uuid import uuid4

from micropy.core.modelling.command import AggregateLifecycle
from proof_of_concept.food_ordering.coreapi.commands import ConfirmOrderCommand
from proof_of_concept.food_ordering.coreapi.commands import CreateFoodCartCommand
from proof_of_concept.food_ordering.coreapi.commands import DeselectProductCommand
from proof_of_concept.food_ordering.coreapi.commands import SelectProductCommand
from proof_of_concept.food_ordering.coreapi.events import FoodCartCreatedEvent
from proof_of_concept.food_ordering.coreapi.events import OrderConfirmedEvent
from proof_of_concept.food_ordering.coreapi.events import ProductDeselectedEvent
from proof_of_concept.food_ordering.coreapi.events import ProductSelectedEvent
from proof_of_concept.food_ordering.coreapi.exceptions import ProductDeselectionException


# @Aggregate
class FoodCart:
    _logger = logging.getLogger('FoodCart')

    # @CommandHandler
    # @AggregateIdentifier('_food_cart_id')
    def __init__(self, command: CreateFoodCartCommand):
        self._food_cart_id: UUID = None
        self._selected_products: MutableMapping[UUID, int] = None
        self._confirmed: bool = None
        AggregateLifecycle.apply(FoodCartCreatedEvent(command.food_cart_id))

    # @CommandHandler
    def handle_select_product(self, command: SelectProductCommand):
        AggregateLifecycle.apply(ProductSelectedEvent(self._food_cart_id, command.product_id, command.quantity))

    # @CommandHandler
    def handle_deselect_product(self, command: DeselectProductCommand):
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

    # @CommandHandler
    def handle_confirm_order(self, command: ConfirmOrderCommand):
        if self._confirmed:
            self._logger.warning("Cannot confirm a Food Cart order which is already confirmed")
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
