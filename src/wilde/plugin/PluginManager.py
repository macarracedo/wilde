from wilde.plugin.Plugin import Plugin
from wilde.plugins.whois.WhoisPlugin import WhoisPlugin


class PluginManager:
    """
    Class responsible for plugin management, including the retrieval of a plugin based on its id.
    """
    def __init__(self):
        # TODO: Plugin registering should be done dynamically
        self._plugins: dict[str, Plugin] = {
            WhoisPlugin.id(): WhoisPlugin()
        }

    def get_plugin(self, plugin_id: str) -> Plugin:
        return self._plugins[plugin_id]
