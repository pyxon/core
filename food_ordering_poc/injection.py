from injector import Injector
from injector import Module


class InjectorConfiguration(Module):
    def configure(self, binder):
        pass


def get_injector() -> Injector:
    global _injector
    if _injector is None:
        _injector = Injector([])
    return _injector


_injector = None
