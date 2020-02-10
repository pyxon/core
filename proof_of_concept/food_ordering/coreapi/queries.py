from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True)
class FindFoodCartQuery:
    food_cart_id: UUID


@dataclass(frozen=True)
class RetrieveProductOptionsQuery:
    pass
