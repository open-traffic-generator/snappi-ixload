import json
import re
import time
from brisk_ixload.timer import Timer

class stats(object):
    """Transforms OpenAPI objects into IxNetwork objects
    - Lag to /lag
    Args
    ----
    - ixnetworkapi (Api): instance of the Api class
    """
    
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """Transform config.ports into Ixnetwork.Vport
        1) delete any vport that is not part of the config
        2) create a vport for every config.ports[] that is not present in IxNetwork
        3) set config.ports[].location to /vport -location using resourcemanager
        4) set /vport/l1Config/... properties using the corrected /vport -type
        5) connectPorts to use new l1Config settings and clearownership
        """
        self._scenarios_config = self._api.brisk_config
        

        with Timer(self._api, "Scenario Configuration"):
            self._create_scenarios()
    
    def _create_scenarios(self):
        """Add any scenarios to the api server that do not already exist
        """
        for scenario in self._scenarios_config:
            url1, url2 = self._api._get_url(self._api._ixload , scenario.url)
            payload = {}
            response = self._api._request('POST', url1, payload)
            new_url = url1 + response + url2
            scenario.url = new_url
            self._create_network(scenario, scenario.url)
            
