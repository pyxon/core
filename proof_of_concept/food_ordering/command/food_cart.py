from collections import defaultdict
from typing import MutableMapping
from uuid import UUID
from uuid import uuid4

from micropy.core.modelling.command import AggregateLifecycle
from proof_of_concept.food_ordering.coreapi.commands import CreateFoodCartCommand
from proof_of_concept.food_ordering.coreapi.commands import DeselectProductCommand
from proof_of_concept.food_ordering.coreapi.commands import SelectProductCommand
from proof_of_concept.food_ordering.coreapi.events import FoodCartCreatedEvent
from proof_of_concept.food_ordering.coreapi.events import ProductDeselectedEvent
from proof_of_concept.food_ordering.coreapi.events import ProductSelectedEvent
from proof_of_concept.food_ordering.coreapi.exceptions import ProductDeselectionException


# @Aggregate
class FoodCart:

    # @CommandHandler
    # @AggregateIdentifier('_food_cart_id')
    def __init__(self, command: CreateFoodCartCommand):
        self._food_cart_id: UUID = None
        self._selected_products: MutableMapping[UUID, int] = None
        AggregateLifecycle.apply(FoodCartCreatedEvent(uuid4()))

    # @CommandHandler
    def handle(self, command: SelectProductCommand):
        AggregateLifecycle.apply(ProductSelectedEvent(self._food_cart_id, command.product_id, command.quantity))

    # @CommandHandler
    def handle(self, command: DeselectProductCommand):
        product_id = command.product_id
        if product_id not in self._selected_products:
            raise ProductDeselectionException()
        AggregateLifecycle.apply(ProductDeselectedEvent(self._food_cart_id, command.product_id, command.quantity))

    # @EventSourcingHandler
    def on(self, event: FoodCartCreatedEvent):
        self._food_cart_id = event.food_cart_id
        self._selected_products = defaultdict(int)

    # @EventSourcingHandler
    def on(self, event: ProductSelectedEvent):
        self._selected_products[event.product_id] += event.quantity
