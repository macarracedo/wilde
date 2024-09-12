from typing import Optional

from wilde.plugins.whois.client.WhoisClient import WhoisClient


class MockWhoisClient(WhoisClient):
    def __init__(self):
        # Domain -> Server -> Data
        self._whois_data: dict[str, dict[str, str]] = {}

    def get_whois_info(self, domain: str, server: str = "whois.iana.org") -> str:
        if domain in self._whois_data and server in self._whois_data[domain]:
            return self._whois_data[domain][server]
        else:
            # TODO: add the standard response of each server for unknown domains
            return "Unknown domain"

    def set_domain_whois(self, domain: str, server: str, whois_data: str) -> None:
        if domain not in self._whois_data:
            self._whois_data[domain] = {server: whois_data}
        else:
            self._whois_data[domain][server] = whois_data

    def set_domain_whois_from_file(self, domain: str, server: str, whois_data_path: str) -> None:
        with open(whois_data_path, "r") as whois_data_file:
            self.set_domain_whois(domain, server, whois_data_file.read())
