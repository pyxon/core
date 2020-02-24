from injector import inject

from pyxon.core.command_handling.gateway import CommandGateway
from ..client import AxonServerClient


class CommandGatewayImpl(CommandGateway):

    @inject
    def __init__(self):
        self._client = AxonServerClient('poc-command-gateway')
        self._client.run()

    def send(self, command):
        self._client.dispatch_command(command)
