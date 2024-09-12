from abc import ABC, abstractmethod

from wilde.operation.Operation import Operation


class Plugin(ABC):
    """
    WILDE plugin's abstract base class that includes methods to retrieve the identifiers of the operations managed by
    the plugin and a method to retrieve a new instance of a plugin, given the parameter values.
    """

    @staticmethod
    @abstractmethod
    def id() -> str:
        """
        The identifier of the plugin. It must be unique for each plugin.

        :return: the identifier of the plugin.
        """
        raise NotImplementedError()

    @abstractmethod
    def list_operations(self) -> list[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_operation(self, operation_id: str, params: dict[str, str]) -> Operation:
        raise NotImplementedError()
