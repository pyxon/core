from typing import Optional

from proof_of_concept.food_ordering.coreapi.events import FoodCartCreatedEvent
from proof_of_concept.food_ordering.coreapi.queries import FindFoodCartQuery
from proof_of_concept.food_ordering.query.food_cart_view import FoodCartView
from proof_of_concept.food_ordering.query.food_cart_view import FoodCartViewRepository


# @Component
class FoodCartProjector:

    def __init__(self, repository: FoodCartViewRepository):
        self._repository = repository

    # @EventHandler
    def on(self, event: FoodCartCreatedEvent):
        food_cart_view = FoodCartView(event.food_cart_id, {})
        self._repository.save(food_cart_view)

    # @QueryHandler
    def handle(self, query: FindFoodCartQuery) -> Optional[FoodCartView]:
        return self._repository.find_by_id(query.food_cart_id)
