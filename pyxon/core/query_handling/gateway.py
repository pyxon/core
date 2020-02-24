from abc import ABCMeta
from abc import abstractmethod


class QueryGateway(metaclass=ABCMeta):

    @abstractmethod
    def query(self, query, response_type):
        pass
