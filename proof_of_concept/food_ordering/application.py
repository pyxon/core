from micropy.core.application import Application
from micropy.core.application_runner import ApplicationRunner


@Application
class FoodOrderingApplication:
    def main(self, *args):
        ApplicationRunner.run(FoodOrderingApplication)
