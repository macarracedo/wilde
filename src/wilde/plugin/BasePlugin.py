from abc import ABC
from typing import Type

from wilde.operation.Operation import Operation
from wilde.plugin.Plugin import Plugin


class BasePlugin(Plugin, ABC):
    """
    WILDE plugin's base helper class, that provides a default implementation of the Plugin methods and that receives a
    dictionary with the identifiers and a builder for the operations.
    """

    def __init__(self, operations: list[Type[Operation]]):
        self._operations: dict[str, Type[Operation]] = {
            operation.id(): operation for operation in operations
        }

    def list_operations(self) -> list[str]:
        return list(self._operations.keys())

    def get_operation(self, operation_id: str, params: dict[str, str]) -> Operation:
        return self._operations[operation_id].build(params)
