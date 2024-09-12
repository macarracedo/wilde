from typing import Type, Final, Optional

from wilde.model import LocationData
from wilde.operation.Operation import Operation
from wilde.plugins.whois.client.DefaultWhoisClient import DefaultWhoisClient
from wilde.plugins.whois.client.WhoisClient import WhoisClient
from wilde.plugins.whois.parser.IANAWhoisParser import IANAWhoisParser
from wilde.plugins.whois.parser.ORGWhoisParser import ORGWhoisParser
from wilde.plugins.whois.parser.GALWhoisParser import GALWhoisParser
from wilde.plugins.whois.parser.WhoisParser import WhoisParser

_IANA_PREFIX: Final[str] = "Whois IANA#"
_REFER_PREFIX: Final[str] = "Whois Refer#"
_IANA_SERVER: Final[str] = "whois.iana.org"
_SERVER_PARSER: Final[dict[str, WhoisParser]] = {
    'whois.iana.org': IANAWhoisParser(),
    'whois.publicinterestregistry.org': ORGWhoisParser(),
    'whois.nic.gal': GALWhoisParser(),
}


class RetrieveWhoisInfoOperation(Operation):
    """
    Operation that retrieves Whois information for a domain.
    """

    @staticmethod
    def id() -> str:
        return "retrieve"

    @staticmethod
    def plugin_id() -> str:
        return "whois"

    @classmethod
    # TODO: Use Self in the future
    def build(cls: Type["RetrieveWhoisInfoOperation"], params: dict[str, str]) -> "RetrieveWhoisInfoOperation":
        return RetrieveWhoisInfoOperation()

    def __init__(self,
                 whois_client: WhoisClient = DefaultWhoisClient(),
                 server_parser: Optional[dict[str, WhoisParser]] = None):
        self._whois_client: WhoisClient = whois_client
        self._server_parser: dict[str, WhoisParser] = \
            server_parser.copy() if server_parser is not None else _SERVER_PARSER.copy()

    def _query_whois(self, domain: str) -> dict[str, str]:
        response_iana = self._whois_client.get_whois_info(domain)
        location_metadata = self._server_parser[_IANA_SERVER].parse_response(response_iana)

        if location_metadata is None:
            return {}

        if f"{_IANA_PREFIX}refer" in location_metadata:
            refer_server = location_metadata[f"{_IANA_PREFIX}refer"]
            response_refer = self._whois_client.get_whois_info(domain, refer_server)
            if response_refer is None:
                location_metadata[f"{_REFER_PREFIX}status"] = "unavailable"
            else:
                refer_location_metadata = self._server_parser[refer_server].parse_response(response_refer)

                if refer_location_metadata is not None:
                    location_metadata.update(refer_location_metadata)

        return location_metadata

    def run(self, location_data: LocationData) -> LocationData:
        response = self._query_whois(location_data.location)

        if response is None:
            location_data.set_data_value(f"{_IANA_PREFIX}status", "unavailable")
        else:
            for key, value in response.items():
                location_data.set_data_value(key, value)

        return location_data

    def __str__(self) -> str:
        return "Retrieve operation from whois plugin"

    def __repr__(self) -> str:
        return f"({self.plugin_id()}.{self.id()})"
