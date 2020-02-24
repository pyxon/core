import threading
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import Optional
from frozendict import frozendict


class CommandHandler(metaclass=ABCMeta):

    @property
    @abstractmethod
    def command(self):
        pass


class AggregateCommandHandler(CommandHandler):

    def __init__(self, aggregate_cls, method):
        self._method = method

    @property
    def command(self):
        return self._method.__handle_command__


class CommandHandlingRegistry:

    _registry_lock = threading.Lock()
    _registry: 'CommandHandlingRegistry' = None

    def __init__(self):
        self._command_handlers = {}
        self._lock = threading.Lock()

    @classmethod
    def get_command_handlers(cls, registry: Optional['CommandHandlingRegistry'] = None) -> Mapping[Any, CommandHandler]:
        if registry is None:
            registry = cls._ensure_registry()

        with registry._lock:
            return frozendict(registry._command_handlers)

    @classmethod
    def register_command_handler(cls, handler: CommandHandler, registry: Optional['CommandHandlingRegistry'] = None):
        if registry is None:
            registry = cls._ensure_registry()

        with registry._lock:
            command = handler.command
            if command in registry._command_handlers:
                raise Exception(f"Command {command} already has a handler")
            registry._command_handlers[command] = handler

    @classmethod
    def _ensure_registry(cls):
        with cls._registry_lock:
            if cls._registry is None:
                cls._registry = cls()
            return cls._registry
