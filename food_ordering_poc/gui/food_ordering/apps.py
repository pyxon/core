from django.apps import AppConfig
from winter.controller import set_controller_factory

from .injection import get_injector


class FoodOrderingApplication(AppConfig):
    name = 'food_ordering'
    verbose_name = 'Food Ordering'

    def ready(self):
        injector = get_injector()
        set_controller_factory(injector.get)
