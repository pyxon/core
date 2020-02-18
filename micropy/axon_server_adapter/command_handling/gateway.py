from injector import inject

from ..client import AxonServerClient


class CommandGatewayImpl:

    @inject
    def __init__(self, axon_server_client: AxonServerClient):
        self._client = axon_server_client
        self._client.run('poc-command-gateway')

    def send(self, command):
        pass
