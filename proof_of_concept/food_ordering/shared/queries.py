from uuid import UUID

from dataclasses import dataclass


@dataclass
class FindFoodCartQuery:
    food_cart_id: UUID


@dataclass
class RetrieveProductOptionsQuery:
    pass
