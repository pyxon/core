from typing import Awaitable
from uuid import UUID
from uuid import uuid4

import winter
from injector import inject

from pyxon.core.command_handling.gateway import CommandGateway
from pyxon.core.messaging.response_types import ResponseTypes
from pyxon.core.query_handling.gateway import QueryGateway
from food_ordering_poc.shared.commands import CreateFoodCartCommand
from food_ordering_poc.shared.commands import DeselectProductCommand
from food_ordering_poc.shared.commands import SelectProductCommand
from food_ordering_poc.shared.queries import FindFoodCartQuery
from food_ordering_poc.query.food_cart_view import FoodCartView


@winter.controller
@winter.route("food_cart/")
@winter.no_authentication
class FoodOrderingController:

    @inject
    def __init__(self, command_gateway: CommandGateway, query_gateway: QueryGateway):
        self._command_gateway = command_gateway
        self._query_gateway = query_gateway

    @winter.route_post("create/")
    def create_food_cart(self) -> Awaitable[UUID]:
        return self._command_gateway.send(CreateFoodCartCommand(uuid4()))

    @winter.route_post("{food_cart_id}/select/{product_id}/quantity/{quantity}/")
    def select_product(self, food_cart_id: UUID, product_id: UUID, quantity: int):
        self._command_gateway.send(SelectProductCommand(food_cart_id, product_id, quantity))

    @winter.route_post("{food_cart_id}/deselect/{product_id}/quantity/{quantity}/")
    def deselect_product(self, food_cart_id: UUID, product_id: UUID, quantity: int):
        self._command_gateway.send(DeselectProductCommand(food_cart_id, product_id, quantity))

    @winter.route_get("{food_cart_id}/")
    def find_food_cart(self, food_cart_id: UUID) -> Awaitable[FoodCartView]:
        return self._query_gateway.query(FindFoodCartQuery(food_cart_id), ResponseTypes.instance_of(FoodCartView))
