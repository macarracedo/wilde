from abc import ABC, abstractmethod


class WhoisClient(ABC):
    """
    Class that represents a Whois Client.
    """

    @abstractmethod
    def get_whois_info(self, domain: str, server: str = "whois.iana.org") -> str:
        """
        Retrieves WHOIS information for a given domain from a specific server.

        :param domain: the domain for which WHOIS information is to be retrieved.
        :param server: the WHOIS server to query for information.
        :return: the WHOIS information as a string.
        """
        raise NotImplementedError("run method not implemented")
