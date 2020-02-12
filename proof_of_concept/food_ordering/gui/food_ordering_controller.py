import winter

from micropy.core.command_handling.gateway import CommandGateway


@winter.controller
class FoodOrderingController:

    def __init__(self, command_gateway: CommandGateway):
        self._command_gateway = command_gateway

    @winter.route_post('create/')
    def create(self):
