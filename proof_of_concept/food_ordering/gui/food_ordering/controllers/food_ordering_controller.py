from typing import Awaitable
from uuid import UUID
from uuid import uuid4

import winter

from micropy.core.command_handling.gateway import CommandGateway
from micropy.core.messaging.response_types import ResponseTypes
from micropy.core.query_handling.gateway import QueryGateway
from proof_of_concept.food_ordering.shared.commands import CreateFoodCartCommand
from proof_of_concept.food_ordering.shared.commands import DeselectProductCommand
from proof_of_concept.food_ordering.shared.commands import SelectProductCommand
from proof_of_concept.food_ordering.shared.queries import FindFoodCartQuery
from proof_of_concept.food_ordering.query.food_cart_view import FoodCartView


@winter.controller
@winter.route("food_cart/")
@winter.no_authentication
class FoodOrderingController:

    def __init__(self, command_gateway: CommandGateway, query_gateway: QueryGateway):
        self._command_gateway = command_gateway
        self._query_gateway = query_gateway

    @winter.route_post("create/")
    def create_food_cart(self):
        self._command_gateway.send(CreateFoodCartCommand(uuid4()))

    @winter.route_post("{food_cart_id}/select/{product_id}/quantity/{quantity}/")
    def select_product(self, food_cart_id: UUID, product_id: UUID, quantity: int):
        self._command_gateway.send(SelectProductCommand(food_cart_id, product_id, quantity))

    @winter.route_post("{food_cart_id}/deselect/{product_id}/quantity/{quantity}/")
    def deselect_product(self, food_cart_id: UUID, product_id: UUID, quantity: int):
        self._command_gateway.send(DeselectProductCommand(food_cart_id, product_id, quantity))

    @winter.route_get("{food_cart_id}/")
    def find_food_cart(self, food_cart_id: UUID) -> Awaitable[FoodCartView]:
        return self._query_gateway.query(FindFoodCartQuery(food_cart_id), ResponseTypes.instance_of(FoodCartView))
