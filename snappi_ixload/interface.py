import json
import re
import time
from .timer import Timer

class interfaces(object):
    """Transforms OpenAPI objects into IxNetwork objects
    - Lag to /lag
    Args
    ----
    - Ixloadapi (Api): instance of the Api class

    """
    _ETHERNET = {
        "mac": "mac",
        "mtu": "mtu",
        "step": "incrementBy",
        #"count": "count"
    }

    _IP = {
        "address": "ipAddress",
        "gateway": "gatewayAddress",
        "prefix": "prefix",
        "name" : "name",
        "step": "incrementBy",
        "count": "count",
    }

    _IPv6 = {
        "address": "ipAddress",
        "gateway": "gatewayAddress",
        "prefix": "prefix",
        "name" : "name",
        "increment_by": "incrementBy",
        "count": "count",
        "gateway_incr": "gatewayIncrement"
    }
    
    _VLAN = {
        "id": "firstId",
        "priority": "priority",
        "tpid": "tpid",
        "name" : "name"
    }
        
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """T
        """
        self._devices_config = self._api._l47config.devices
        with Timer(self._api, "Interface Configuration"):
            self._create_devices()
    
    def _create_devices(self):
        """Add any scenarios to the api server that do not already exist
        """
        for device in self._devices_config:
            url1 = self._api._ixload + "ixload/test/activeTest/communityList"
            payload = {}
            response = self._api._request('POST', url1, payload)
            new_url = url1 + "/" + response + "/network/stack/childrenList"
            self._api._config_url[device.name] = new_url
            #self._delete_ethernet(device, new_url)
        for device in self._devices_config:
            self._create_ethernet(device)
            #self._create_ipv4()
            
  
    def _create_ethernet(self, device):       
        """Add any scenarios to the api server that do not already exist
        """
        flag = 1
        for ethernet in device.ethernets:
            if flag:
                #payload = {"itemType": "L2EthernetPlugin"}
                url = self._api._config_url[device.name]
                response = self._api._request('GET', url)
                self._api._config_url["mac_url"] = url + "/" + str(response[-1]['objectID'])
                eth_url = url + "/" + str(response[-1]['objectID']) + "/macRangeList/"
                ipp_url = url + "/" + str(response[-1]['objectID']) + "/childrenList/"
                mac_url =  eth_url + str(self._api._request('GET', eth_url)[-1]['objectID'])
                ip_url =  ipp_url + str(self._api._request('GET', ipp_url)[-1]['objectID']) + "/rangeList/"
                ip_url = ip_url + str(self._api._request('GET', ip_url)[-1]['objectID'])
                
                vlan_url = url + "/" + str(response[-1]['objectID']) + "/vlanRangeList/"
                vlan_url =  vlan_url + str(self._api._request('GET', vlan_url)[-1]['objectID'])
                payload = {"autoMacGeneration": False}
                response = self._api._request('PATCH', ip_url, payload)
                payload = self._api._set_payload(ethernet, interfaces._ETHERNET)
                response = self._api._request('PATCH', mac_url, payload)
                self._api._config_url[ethernet.name] = mac_url
                self._create_ipv4(ethernet, ip_url, flag)
                self._create_ipv6(ethernet, ip_url,flag)
                self._create_vlan(ethernet, vlan_url, flag)
                flag = 0
            else:
                eth_url = self._api._config_url["mac_url"] + "/macRangeList"
                payload = self._api._set_payload(ethernet, interfaces._ETHERNET)
                response = self._api._request('POST', eth_url, payload)
                eth_url = eth_url + "/" + str(response)
                ip_url = self._api._config_url["mac_url"] + "/childrenList/"
                ip_url = ip_url + str(self._api._request('GET', ip_url, option=1)[-1]['objectID']) + "/rangeList/"
                ip_url = ip_url + str(self._api._request('GET', ip_url, option=1)[-1]['objectID'])
                
                vlan_url = self._api._config_url["mac_url"] + "/vlanRangeList/"
                vlan_url = vlan_url + str(self._api._request('GET', vlan_url, option=1)[-1]['objectID'])
                payload = {"autoMacGeneration": False}
                response = self._api._request('PATCH', ip_url, payload)
                self._api._config_url[ethernet.name] = eth_url
                self._create_ipv4(ethernet, ip_url, flag)
                self._create_ipv6(ethernet, ip_url,flag)
                self._create_vlan(ethernet, vlan_url, flag)
            

    def _delete_ethernet(self, device, url):
        """delete any scenarios to the api server that do not already exist
        """
        response = self._api._request('GET', url, option=1)
        payload = {'objectID':response[0]['objectID']}
        response = self._api._request('DELETE', url, payload)


    def _create_ipv4(self, ethernet, url, flag):
        """
            Add any ipv4 to the api server that do not already exist
        """
        ipv4_addresses = ethernet.get("ipv4_addresses")
        if ipv4_addresses is None:
            return
        for ipv4 in ethernet.ipv4_addresses: 
            payload = self._api._set_payload(ipv4, interfaces._IP)
            if payload:
                response = self._api._request('PATCH', url, payload)
                self._api._config_url[ipv4.name] = url

    def _create_ipv6(self, ethernet, url, flag):
        """
            Add any ipv6 to the api server that do not already exist
        """
        ipv6_addresses = ethernet.get("ipv6_addresses")
        if ipv6_addresses is None:
            return
        for ipv6 in ethernet.ipv6_addresses: 
            payload = self._api._set_payload(ipv6, interfaces._IPv6)
            payload['ipType'] = "IPv6"
            # payload['gatewayIncrement'] = '::0'  # need to update model
            # payload['incrementBy'] = '::1'   #need to update model
            if payload:
                response = self._api._request('PATCH', url, payload)
                self._api._config_url[ipv6.name] = url
    
    def _create_vlan(self, ethernet, vlan_url, flag):
        """
            Add any ipv4 to the api server that do not already exist
        """
        
        vlans = ethernet.get("vlans")
        if vlans is None:
            return
        for vlan in ethernet.vlans:
            payload = {"enabled": True}
            response = self._api._request('PATCH', vlan_url, payload)
            payload = self._api._set_payload(vlan, interfaces._VLAN)
            if payload:
                if 'tpid' in payload.keys():
                    payload['tpid'] = "0" + payload['tpid']
                response = self._api._request('PATCH', vlan_url, payload)
                self._api._config_url[vlan.name] = vlan_url
