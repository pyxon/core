from uuid import UUID

from dataclasses import dataclass


@dataclass
class FoodCartCreatedEvent:
    food_cart_id: UUID


@dataclass
class ProductSelectedEvent:
    food_cart_id: UUID
    product_id: UUID
    quantity: int


@dataclass
class ProductDeselectedEvent:
    food_cart_id: UUID
    product_id: UUID
    quantity: int


@dataclass
class OrderConfirmedEvent:
    food_cart_id: UUID
