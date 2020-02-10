from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True)
class FoodCartCreatedEvent:
    food_cart_id: UUID


@dataclass(frozen=True)
class ProductSelectedEvent:
    food_cart_id: UUID
    product_id: UUID
    quantity: int


@dataclass(frozen=True)
class ProductDeselectedEvent:
    food_cart_id: UUID
    product_id: UUID
    quantity: int


@dataclass(frozen=True)
class OrderConfirmedEvent:
    food_cart_id: UUID
