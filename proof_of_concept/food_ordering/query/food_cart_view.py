from dataclasses import dataclass
from typing import MutableMapping
from uuid import UUID

from persipy import CRUDRepository


# @Entity
@dataclass
class FoodCartView:
    # @Id
    food_cart_id: UUID
    # @ElementCollection
    products: MutableMapping[UUID, int]

    def add_products(self, product_id: UUID, amount: int):
        if product_id not in self.products:
            self.products[product_id] = 0
        self.products[product_id] += amount

    def remove_products(self, product_id: UUID, amount: int):
        self.products[product_id] -= amount
        if self.products[product_id] == 0:
            del self.products[product_id]


class FoodCartViewRepository(CRUDRepository[FoodCartView, UUID]):
    pass
