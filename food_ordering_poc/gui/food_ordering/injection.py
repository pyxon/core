from injector import Injector
from injector import Module

from micropy.axon_server_adapter.command_handling import CommandGatewayImpl
from micropy.axon_server_adapter.query_handling import QueryGatewayImpl
from micropy.core.command_handling.gateway import CommandGateway
from micropy.core.query_handling.gateway import QueryGateway


class InjectorConfiguration(Module):
    def configure(self, binder):
        binder.bind(CommandGateway, CommandGatewayImpl)
        binder.bind(QueryGateway, QueryGatewayImpl)


def get_injector() -> Injector:
    global _injector
    if _injector is None:
        _injector = Injector([InjectorConfiguration])
    return _injector


_injector = None
