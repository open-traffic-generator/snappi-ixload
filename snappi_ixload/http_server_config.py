import json
import re
import time
from snappi_ixload.timer import Timer

class server_config():
    """
    """
    _HTTP_SERVER = {
        "enable_tos" : "enableTos",
        #"priority_flow_control_class" : "pfcClass",
        #"precedence_tos" : "precedenceTOS",
        #"delay_tos" : "delayTOS",
        #"throughput_tos"  : "throughputTOS",
        "url_stats_count" : "urlStatsCount",
        "disable_priority_flow_control" : "disablePfc",
        "enable_vlan_priority" : "enableVlanPriority",
        "vlan_priority" : "vlanPriority",
        "esm" : "esm",
        "enable_esm" : "enableEsm",
        "time_to_live_value" : "ttlValue",
        #"tcp_close_option" : "tcpCloseOption",
        "type_of_service" : "tos",
        "high_perf_with_simulated_user" : "highPerfWithSU"
    }

    _HTTP_SERVERS = {
        "rst_timeout" : "rstTimeout",
        "enable_http2" : "enableHTTP2",
        "port" : "httpPort",
        "request_timeout" : "requestTimeout",
        "maximum_response_delay" : "maxResponseDelay",
        "minimum_response_delay" : "minResponseDelay",
        "dont_expect_upgrade" : "dontExpectUpgrade",
        "enable_per_server_per_url_stat" : "enablePerServerPerURLstat",
        "url_page_size" : "urlPageSize",
        "enable_chunk_encoding" : "enableChunkEncoding",
        #"integrity_check_option" : "integrityCheckOption",
        "enable_md5_checksum" : "enableMD5Checksum",
    }

    _TCP = {
        "keep_alive_time": "tcp_keepalive_time"
    }
        
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """
        """
        self._devices_config = self._api._l47config.devices
        with Timer(self._api, "HTTP server Configurations"):
            self._create_server_app()
    
    def _create_server_app(self):
        """Add any scenarios to the api server that do not already exist
        """
        for device in self._devices_config:
            self._create_http_server(device)
            
    def _create_http_server(self, device):
        """Add any scenarios to the api server that do not already exist
        """
        for http in device.https:
            for http_server in http.servers:
            #ip_object = self._ip_list(server.server.name)
            #ip_object = "e2.ipv4"
                url = self._api._config_url.get(http.tcp_name)
                url = self._api.common.get_community_url(url)
                #url = self._api._ixload+"ixload/test/activeTest/communityList/1"
                protocol_url = url+"activityList/"
                options = {}
                options.update({'protocolAndType': "HTTP Server"})
                response = self._api._request('POST', protocol_url, options)
                protocol_url = protocol_url+response
                #self._api._config_url[server.server.name] = protocol_url
                payload = self._api._set_payload(http, server_config._HTTP_SERVER)
                response = self._api._request('PATCH', protocol_url+"/agent", payload)
                payload = self._api._set_payload(http_server, server_config._HTTP_SERVERS)
                response = self._api._request('PATCH', protocol_url+"/agent", payload)
            del(http)
            #self._update_tcp_server(app_config, server)
    
    def _update_tcp_server(self, app_config, server):
        #ip_object = self._api.common.get_ip_name(self._server_config, server.server.name)
        for tcp in app_config.tcp:
            url = self._api._config_url.get(self._api._ip_list.get(server.server.name))
            #url = self._api._config_url.get(ip_object)
            url = self._api.common.get_community_url(url)
            tcp_child_url = "%snetwork/globalPlugins" % url
            response_list = self._api._request('GET', tcp_child_url)
            for index in range(len(response_list)):
                if response_list[index]['itemType'] == 'TCPPlugin':
                    tcp_url = "%s/%s" % (tcp_child_url, response_list[index]['objectID'])
                    payload = self._api._set_payload(tcp, server_config._TCP)
                    response = self._api._request('PATCH', tcp_url, payload)


