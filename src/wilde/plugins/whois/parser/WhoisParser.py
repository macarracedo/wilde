from abc import ABC, abstractmethod
from typing import Optional


class WhoisParser(ABC):
    @abstractmethod
    def parse_response(self, response: str) -> Optional[dict[str, str]]:
        """
        Parses a Whois response and returns a dictionary with the metadata.

        :param response: the response to be parsed.
        :return: a dictionary with the metadata parsed from the response. None if there was no response.
        """
        pass
