from abc import ABC, abstractmethod
from typing import Type

from wilde.model import LocationData


class Operation(ABC):
    """
    Class that represents an operation over a location.
    """

    @staticmethod
    @abstractmethod
    def id() -> str:
        """
        The identifier of the operation. It must be unique for each different operation in a plugin.

        :return: the identifier of the operation.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def plugin_id() -> str:
        """
        The identifier of the plugin. It must be unique for each plugin.

        :return: the identifier of the plugin.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def build(cls: Type["Operation"], params: dict[str, str]) -> "Operation":  # TODO: Use Self in the future
        """
        Builds an instance of the current operation using the received parameters.
        :param params: parameters to assign to the newly created instance of the operation.
        :return: a new instance of the current operation configured with the received parameters.
        """
        raise NotImplementedError()

    @abstractmethod
    def run(self, location_data: LocationData) -> LocationData:
        """
        Performs an operation over the location and, ideally, adds new metadata to it.

        :param location_data: the location to which the operation is to be applied.
        :return: the location_data received as parameter, likely with new metadata.
        """
        raise NotImplementedError("run method not implemented")
