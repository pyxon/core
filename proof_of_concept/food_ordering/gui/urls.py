from winter.django import create_django_urls

from .controllers.food_ordering_controller import FoodOrderingController

urlpatterns = [
    *create_django_urls(FoodOrderingController),
]
