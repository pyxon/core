from abc import ABCMeta
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


class FoodCartViewRepository(CRUDRepository[FoodCartView, UUID], metaclass=ABCMeta):
    pass
