import json
import re
import time
from timer import Timer


class trafficmap_config():
    """Traffic map class config
    """

    _POLICY_CONFIG= {"port_map_policy_name": "portMapPolicy"}

    _POLICY_CONFIG_NAME = { 
        "custom": "customMesh",
        "port_pairs": "portPairs",
        "full_mesh": "portMesh"
    }

    _CUSTOM_CONFIG = {
        "name": "name"
    }

    _PAIRS_TYPE = {
        "enable": "enable",
        "destination_id": "destinationId"
    }

    _MESH_TYPE = {"enable": "enable"}

    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """
        """
        self._config = self._api._l47config
        with Timer(self._api, "Traffic map Configurations"):
            for device in self._config.devices:
                for http in device.https:
                    for http_client in http.clients:
                        self._configure_trafficmap_config(http_client)

    def _configure_trafficmap_config(self, http_client):
        """Add any scenarios to the api server that do not already exist
        """
        for trafficprofile in self._config.trafficprofile:
            url = self._api._config_url.get(http_client.name)
            if trafficprofile.trafficmap and http_client.name == trafficprofile.app[0]:
                for trafficmap in trafficprofile.trafficmap:
                    map_url = "%s/destinations/0" % (url)
                    payload = self._api._set_payload(trafficmap, trafficmap_config._POLICY_CONFIG)
                    payload['portMapPolicy'] = trafficmap_config._POLICY_CONFIG_NAME[payload['portMapPolicy']]
                    response = self._api._request('PATCH', map_url, payload)
                    if payload['portMapPolicy'] == "customMesh":
                        customipv4_url = "%s/customPortMap/submapsIPv4" %(map_url)
                        response = self._api._request('GET', customipv4_url, {})
                        if len(response) > 0:
                            self._configure_custom_config(customipv4_url, trafficmap, response)
                        else:
                            customipv6_url = "%s/customPortMap/submapsIPv6" %  (map_url)
                            response = self._api._request('GET', customipv6_url, {})
                            self._configure_custom_config(customipv6_url, trafficmap, response)
        return

    def _configure_custom_config(self, url, trafficmap, custom_list):   
        for custom in trafficmap.custom:
            src_payload = {}
            payload = self._api._set_payload(custom, trafficmap_config._CUSTOM_CONFIG)
            meshtype = json.dumps(str(custom.mapping_type))
            if "ip_range_pairs" in meshtype:
                payload['meshType'] = "ipRangePairs"
                src_payload = self._api._set_payload(custom.mapping_type.ip_range_pairs, trafficmap_config._PAIRS_TYPE)
            if "ip_range_mesh" in meshtype:
                payload['meshType'] = "ipRangeMesh"
                src_payload = self._api._set_payload(custom.mapping_type.ip_range_mesh, trafficmap_config._MESH_TYPE)
            if "vlan_range_mesh" in meshtype:
                payload['meshType'] = "vlanRangeMesh"
                src_payload = self._api._set_payload(custom.mapping_type.vlan_range_mesh, trafficmap_config._MESH_TYPE)
            if "vlan_range_pairs" in meshtype:
                payload['meshType'] = "vlanRangePairs"
                src_payload = self._api._set_payload(custom.mapping_type.vlan_range_pairs, trafficmap_config._PAIRS_TYPE)
            response = self._api._request('PATCH', url, payload)
            obj_id = self._get_objectid(payload['name'], url)
            src_url = "%s/%s/sourceRanges" % (url, obj_id) 
            response = self._api._request('PATCH', src_url, src_payload)

    def _get_objectid(self, name, url):
        response = self._api._request('GET', url, {})
        for custom_item in response:
            if name == custom_item['name']:
                return custom_item['objectID']