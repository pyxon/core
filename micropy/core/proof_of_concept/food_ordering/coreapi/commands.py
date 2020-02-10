from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateFoodCartCommand:
    pass


@dataclass(frozen=True)
# @target_aggregate_identifier('food_cart_id')
class SelectProductCommand:
    food_cart_id: UUID
    product_id: UUID
    quantity: int


@dataclass(frozen=True)
# @target_aggregate_identifier('food_cart_id')
class DeselectProductCommand:
    food_cart_id: UUID
    product_id: UUID
    quantity: int


@dataclass(frozen=True)
# @target_aggregate_identifier('food_cart_id')
class ConfirmOrderCommand:
    food_cart_id: UUID
