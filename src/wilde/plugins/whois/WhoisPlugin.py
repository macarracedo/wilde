from wilde.plugin.BasePlugin import BasePlugin
from wilde.plugins.whois.operation.RetrieveWhoisInfoOperation import RetrieveWhoisInfoOperation


class WhoisPlugin(BasePlugin):
    """
    Plugin class for Whois. This plugin only includes the "retrieve" operation, that retrieves the Whois data available
    for a given location.
    """

    @staticmethod
    def id() -> str:
        return "whois"

    def __init__(self):
        super().__init__([RetrieveWhoisInfoOperation])
