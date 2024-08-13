import json
import re
import time
from snappi_ixload.timer import Timer

class port(object):
    """
    Args
    ----
    - Ixloadapi (Api): instance of the Api class

    """
        
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """T
        """
        self._config = self._api._l47config
        with Timer(self._api, "Port Configuration"):
            self._create_chassis()
    
    def _create_chassis(self):
        """Add any scenarios to the api server that do not already exist
        """
        for device in self._config.devices:
            ethernet = device.ethernets[0]
            location = self._get_chasiss(ethernet.connection.port_name, self._config.ports)
            self._add_chassis(location)
            for ip in ethernet.ipv4_addresses:
                self._assign_ports(location, ip.name)
    
    def _get_chasiss(self, port_name, port_config):
        '''
        '''
        for port in port_config:
            if port.name == port_name:
                return port.location
            
    def _add_chassis(self, location):
        '''
        '''
        #
        chassis_name = location.split("/")[0]
        chassis_list_url = "%s/ixload/chassisChain/chassisList" % (self._api._ixload)
        payload = {"name": chassis_name}
        response = self._api._request('POST', chassis_list_url, payload)
        refresh_connection_url = "%s/%s/operations/refreshConnection" % (chassis_list_url, response)
        response = self._api._request('POST', refresh_connection_url, {})
        time.sleep(10)
        #self._api._wait_for_action_to_finish(response, refresh_connection_url)
    
    def _assign_ports(self, location, ip_name):
        '''
        
        '''
        active_test_url = "%s/ixload/test/activeTest" % (self._api._ixload)
        payload = {"enableForceOwnership": "true"}
        self._api._request('PATCH', active_test_url, payload)
        url = self._api._config_url.get(ip_name)
        url = self._api.common.get_community_url(url)
        port_list_url = url + "network/portList"
        chassis_id = 1
        chassis_ip, card_id, port_id = location.split("/")
        payload = {"chassisId": chassis_id, "cardId": card_id, "portId": port_id}
        #import pdb;pdb.set_trace()
        self._api._request('POST', port_list_url, payload)
            
            