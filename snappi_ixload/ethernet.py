import json
import re
from timer import Timer


class ethernet(object):
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
        self._scenarios = self._api.snappi_config.scenarios
        with Timer(self._api, "Ethernet Configuration"):
            for scenario in self._scenarios:
                network = scenario.networks[-1]
                self._delete_ethernet(network)
                self._create_ethernet(network)
          
    
    def _create_ethernet(self, network):
        """Add any scenarios to the api server that do not already exist
        """
        for ethernet in network.ethernet:
            url1, url2 = self._api._get_url(network.url , ethernet.url)
            payload = {"itemType": "L2EthernetPlugin"}
            response = self._api._request('POST', url1, payload)
            ethernet.url = url1 + response + url2
            if network.ipv4:
                self._create_ipv4(network, ethernet.url)
            

    def _delete_ethernet(self, network):
        """delete any scenarios to the api server that do not already exist
        """
        for ethernet in network.ethernet:
            url1, url2 = self._api._get_url(network.url , ethernet.url)
            response = self._api._request('GET', url1, option=1)
            payload = {'objectID':response[0]['objectID']}
            response = self._api._request('DELETE', url1, payload)


    def _create_ipv4(self, network, ethernet_url):
        """
            Add any ipv4 to the api server that do not already exist
        """
        for ipv4 in network.ipv4:
            ipv4_url = ipv4.url
            eth_url = ethernet_url.replace('macRangeList', "")
            url1, url2 = self._api._get_url(eth_url, ipv4_url)
            payload = {"itemType": "IpV4V6Plugin"}
            response = self._api._request('POST', url1, payload)
            ipv4.url = url1 + response + url2
            payload = self._api._set_payload(ipv4)
            if payload:
                self._api._request('PATCH', ipv4.url, payload)
            return