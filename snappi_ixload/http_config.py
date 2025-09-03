import json
import re
import time
from .timer import Timer


class client_config():
    """
    """
    _HTTP_CLIENT = {
        "enable_tos" : "enableTos",
        # "priority_flow_control_class" : "pfcClass",
        # "precedence_tos" : "precedenceTOS",
        # "delay_tos" : "delayTOS",
        #"throughput_tos"  : "throughputTOS",
        #"reliability_tos"  : "reliabilityTOS",
        "url_stats_count" : "urlStatsCount",
        "disable_priority_flow_control" : "disablePfc",
        "enable_vlan_priority" : "enableVlanPriority",
        "vlan_priority" : "vlanPriority",
        "esm" : "esm",
        "enable_esm" : "enableEsm",
        "time_to_live_value" : "ttlValue",
        #"tcp_close_option" : "tcpCloseOption",
        #"enable_integrity_check_support" : "enableIntegrityCheckSupport",
        "type_of_service" : "tos",
        "high_perf_with_simulated_user" : "highPerfWithSU"       
    } 
    _HTTP_CLIENTS = {
        "version" : "httpVersion",
        "cookie_jar_size": "cookieJarSize",
        "cookie_reject_probability" : "cookieRejectProbability",
        "enable_cookie_support" : "enableCookieSupport",
        "command_timeout" : "commandTimeout",
        "command_timeout_ms" : "commandTimeout_ms",
        "enable_proxy" : "enableHttpProxy",
        #"proxy" : "httpProxy",
        "keep_alive" : "keepAlive",
        "max_sessions" : "maxSessions",
        "max_streams" : "maxStreams",
        "max_pipeline" : "maxPipeline",
        "max_persistent_requests" : "maxPersistentRequests",
        "exact_transactions" : "exactTransactions",
        "follow_http_redirects" : "followHttpRedirects",
        "enable_decompress_support" : "enableDecompressSupport",
        "enable_per_conn_cookie_support" : "enablePerConnCookieSupport",
        #"ip_preference" : "ipPreference",
        "enable_large_header" : "enableLargeHeader",
        "max_header_len" : "maxHeaderLen",
        "per_header_percent_dist" : "perHeaderPercentDist",
        "enable_auth" : "enableAuth",
        "piggy_back_ack" : "piggybackAck",
        "tcp_fast_open" : "tcpFastOpen",
        "content_length_deviation_tolerance" : "contentLengthDeviationTolerance",
        "disable_dns_resolution_cache" : "disableDnsResolutionCache",
        "enable_consecutive_ips_per_session" : "enableConsecutiveIpsPerSession",
        "enable_achieve_cc_first" : "enableAchieveCCFirst",
        "enable_traffic_distribution_for_cc" : "enableTrafficDistributionForCC",
        "browser_emulation_name" : "browserEmulationName"
    }
    _HTTP_GET = {
        "destination": "destination",
        "page"  : "pageObject",
        #"abort" : "abort",
        "profile" : "profile",
        "name_value_args": "namevalueargs",
        "enable_direct_server_return" : "enableDi"
    }

    _HTTP_DELETE = {
        "destination" : "destination",
        "page" : "pageObject",
        "abort" : "abort",
        "profile" : "profile"
    }

    _HTTP_POST = {
        "destination": "destination",
        "page"  : "pageObject",
        "abort" : "abort",
        "profile" : "profile",
        "name_value_args": "namevalueargs",
        "arguments" : "arguments",
        "sending_chunk_size" :  "sendingChunkSize",
        "send_md5_chksum_header": "sendMD5ChkSumHeader"
   }
    _HTTP_PUT = {
        "destination": "destination",
        "page"  : "pageObject",
        "abort" : "abort",
        "profile" : "profile",
        "name_value_args": "namevalueargs",
        "arguments" : "arguments",
        "sending_chunk_size" :  "sendingChunkSize",
        "send_md5_check_sum_header": "sendMD5ChkSumHeader"
   }
    _HTTP_HEADER = {
        "destination": "destination",
        "page"  : "pageObject",
        "abort" : "abort",
        "profile" : "profile",
        "name_value_args": "namevalueargs"
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
        with Timer(self._api, "HTTP client Configurations"):
            self._create_client_app()
    
    def _create_client_app(self):
        """Add any scenarios to the api server that do not already exist
        """
        for device in self._devices_config:
            self._create_http_client(device)
            
    def _create_http_client(self, device):
        """Add any scenarios to the api server that do not already exist
        """
        #
        for http in device.https:
            for http_client in http.clients:
            #ip_object = self._ip_list(server.server.name)
            #ip_object = "e2.ipv4"
                url = self._api._config_url.get(http.tcp_name)
                url = self._api.common.get_community_url(url)
                #url = self._api._ixload+"ixload/test/activeTest/communityList/1"
                protocol_url = url+"activityList/"
                options = {}
                options.update({'protocolAndType': "HTTP Client"})
                response = self._api._request('POST', protocol_url, options)
                protocol_url = protocol_url+response
                #self._api._config_url[server.server.name] = protocol_url
                self._api._config_url[http_client.name] = protocol_url
                payload = {'name' : http_client.name}
                response = self._api._request('PATCH', protocol_url, payload)
                payload = self._api._set_payload(http, client_config._HTTP_CLIENT)
                response = self._api._request('PATCH', protocol_url+"/agent", payload)
                payload = self._api._set_payload(http_client, client_config._HTTP_CLIENTS)
                response = self._api._request('PATCH', protocol_url+"/agent", payload)
                self._create_method(http_client, protocol_url)

        # for client in app_config.http_client:
        #     ip_object = self._api.common.get_ip_name(client.client.name)
        #     url = self._api._config_url.get(self._api._ip_list.get(client.client.name))
        #     url = self._api.common.get_community_url(url)
        #     protocol_url = url+"activityList/"
        #     options = {}
        #     options.update({'protocolAndType': "HTTP Client"})
        #     response = self._api._request('POST', protocol_url, options)
        #     protocol_url = protocol_url+response
        #     self._api._config_url[client.client.name] = protocol_url
        #     payload = self._api._set_payload(client.client, client_config._HTTP_CLIENT)
        #     response = self._api._request('PATCH', protocol_url+"/agent", payload)
        #     self._update_tcp_client(app_config, client)
        #     self._create_method(app_config, client, protocol_url)
        # return
        
    def _update_tcp_client(self, app_config, client):
        #ip_object = self._api.common.get_ip_name(client.client.name)
        for tcp in app_config.tcp:
            #url = self._api._config_url.get(ip_object)
            url = self._api._config_url.get(self._api._ip_list.get(client.client.name))
            url = self._api.common.get_community_url(url)
            tcp_child_url = "%snetwork/globalPlugins" % url
            response_list = self._api._request('GET', tcp_child_url)
            for index in range(len(response_list)):
                if response_list[index]['itemType'] == 'TCPPlugin':
                    tcp_url = "%s/%s" % (tcp_child_url, response_list[index]['objectID'])
                    payload = self._api._set_payload(tcp, client_config._TCP)
                    response = self._api._request('PATCH', tcp_url, payload)

    
    def _create_method(self, http_client, protocol_url):
        for method in http_client.methods:
            for post in method.post:
                payload = self._api._set_payload(post, client_config._HTTP_POST)
                payload.update({'commandType':'POST'})
                command_url = protocol_url+"/agent/actionList"
                response = self._api._request('POST', command_url, payload)
            for get in method.get:
                payload = self._api._set_payload(get, client_config._HTTP_GET)
                payload.update({'commandType':'GET'})
                command_url = protocol_url+"/agent/actionList"
                response = self._api._request('POST', command_url, payload)
            for delete in method.delete:
                payload = self._api._set_payload(delete, client_config._HTTP_DELETE)
                payload.update({'commandType':'DELETE'})
                command_url = protocol_url+"/agent/actionList"
                response = self._api._request('POST', command_url, payload)
            for put in method.put:
                payload = self._api._set_payload(put, client_config._HTTP_PUT)
                payload.update({'commandType':'PUT'})
                command_url = protocol_url+"/agent/actionList"
                response = self._api._request('POST', command_url, payload)
            for header in method.header:
                payload = self._api._set_payload(header, client_config._HTTP_HEADER)
                payload.update({'commandType':'HEAD'})
                command_url = protocol_url+"/agent/actionList"
                response = self._api._request('POST', command_url, payload)




