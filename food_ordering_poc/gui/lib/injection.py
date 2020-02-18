from injector import Injector


def get_injector() -> Injector:
    global _injector
    if _injector is None:
        _injector = Injector([])
    return _injector


_injector = None
