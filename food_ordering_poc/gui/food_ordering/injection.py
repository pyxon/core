from injector import Injector
from injector import Module
from injector import singleton

from pyxon.axon_server_adapter.command_handling import CommandGatewayImpl
from pyxon.axon_server_adapter.query_handling import QueryGatewayImpl
from pyxon.core.command_handling.gateway import CommandGateway
from pyxon.core.query_handling.gateway import QueryGateway


class InjectorConfiguration(Module):
    def configure(self, binder):
        binder.bind(CommandGateway, CommandGatewayImpl, scope=singleton)
        binder.bind(QueryGateway, QueryGatewayImpl, scope=singleton)


def get_injector() -> Injector:
    global _injector
    if _injector is None:
        _injector = Injector([InjectorConfiguration])
    return _injector


_injector = None
