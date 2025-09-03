import json
import re
from .timer import Timer


class ipv4(object):
    """Transforms OpenAPI objects into IxLoad objects
    - ipv4 to /ipv4
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
        with Timer(self._api, "Ipv4 Configuration"):
            for scenario in self._scenarios:
                network = scenario.networks[-1]
                self._create_ipv4(network)
    

    def _delete_ipv4(self, network):
        for ipv4 in network.ipv4:
            ipv4_url = ipv4.url
            ethernet_url = network.ethernet.url.replace('macRangeList', "")
            url1, url2 = self._api._get_url(ethernet_url, ipv4_url)
            response = self._api._request('GET', url1, option=1)
            payload = {'objectID':response[0]['objectID']}
            self._api._request('DELETE', url1, payload)
          

    def _create_ipv4(self, network):
        """
            Add any ipv4 to the api server that do not already exist
        """
        for ipv4 in network.ipv4:
            ipv4_url = ipv4.url
            print(network)
            ethernet_url = ethernet_url.replace('macRangeList', "")
            url1, url2 = self._api._get_url(ethernet_url, ipv4_url)
            payload = {"itemType": "IpV4V6Plugin"}
            response = self._api._request('POST', url1, payload)
            ipv4.url = url1 + response + url2
            payload = self._api._set_payload(ipv4)
            if payload:
                self._api._request('PATCH', ipv4.url, payload)