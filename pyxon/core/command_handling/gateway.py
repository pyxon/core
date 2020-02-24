from abc import ABCMeta
from abc import abstractmethod


class CommandGateway(metaclass=ABCMeta):

    @abstractmethod
    def send(self, command):
        pass
