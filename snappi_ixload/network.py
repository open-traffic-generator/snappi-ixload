import json
import re
from .timer import Timer


class network(object):
    """Transforms OpenAPI objects into IxLoad objects
    - network to /network
    Args
    ----
    - ixloadapi (Api): instance of the Api class
    """
    
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """Transform config.network into IxLoad.network
        1) create a network for every config.scenarios.networks that is not present in IxLoad
        2) set config.networks[].name to /network -name using rest call
        """
        self._scenarios = self._api.snappi_config.scenarios
        with Timer(self._api, "Network Configuration"):
            for scenario in self._scenarios:
                self._create_network(scenario)
    
    def _create_network(self, scenario):
        """Add any network to the api server that do not already exist
        """
        for network in scenario.networks:
            url = network.url
            scenario_url = scenario.url
            network_url = scenario_url + '/' + url
            network.url = network_url
            payload = self._api._set_payload(network)
            if payload:
                self._api._request('PATCH', network_url, payload)
