from typing import Optional

from proof_of_concept.food_ordering.shared.events import FoodCartCreatedEvent
from proof_of_concept.food_ordering.shared.events import ProductDeselectedEvent
from proof_of_concept.food_ordering.shared.events import ProductSelectedEvent
from proof_of_concept.food_ordering.shared.queries import FindFoodCartQuery
from proof_of_concept.food_ordering.query.food_cart_view import FoodCartView
from proof_of_concept.food_ordering.query.food_cart_view import FoodCartViewRepository


# @Component
class FoodCartProjector:

    def __init__(self, food_cart_view_repository: FoodCartViewRepository):
        self._food_cart_view_repository = food_cart_view_repository

    # @EventHandler
    def on_food_cart_created(self, event: FoodCartCreatedEvent):
        food_cart_view = FoodCartView(event.food_cart_id, {})
        self._food_cart_view_repository.save(food_cart_view)

    # @EventHandler
    def on_product_selected(self, event: ProductSelectedEvent):
        food_cart_view = self._food_cart_view_repository.find_by_id(event.food_cart_id)
        if food_cart_view:
            food_cart_view.add_products(event.product_id, event.quantity)

    # @EventHandler
    def on_product_deselected(self, event: ProductDeselectedEvent):
        food_cart_view = self._food_cart_view_repository.find_by_id(event.food_cart_id)
        if food_cart_view:
            food_cart_view.remove_products(event.product_id, event.quantity)

    # @QueryHandler
    def handle_find_food_cart(self, query: FindFoodCartQuery) -> Optional[FoodCartView]:
        return self._food_cart_view_repository.find_by_id(query.food_cart_id)
