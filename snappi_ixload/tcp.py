import json
import re
import time
from .timer import Timer
from .common import Common

class tcp_config(Common):
    """Transforms OpenAPI objects into IxNetwork objects
    - Lag to /lag
    Args
    ----
    - Ixloadapi (Api): instance of the Api class

    """
    _HTTP_CLIENT = {
        "command_timeout": "commandTimeout"
    }

    _IP = {
        "address": "ipAddress",
        "gateway": "gatewayAddress",
        "prefix": "prefix",
        "name" : "name"
    }
    _TCP_EN = {
        "adjust_tcp_buffers" : "adjust_tcp_buffers",
    }
    _TCP = {
        "keep_alive_time": "tcp_keepalive_time",
        "keep_alive_interval" : "tcp_keepalive_intvl",
        "receive_buffer_size" : "tcp_rmem_default",
        "transmit_buffer_size" : "tcp_wmem_default",
        "retransmission_minimum_timeout" : "tcp_rto_min",
        "retransmission_maximum_timeout" : "tcp_rto_max",
        "minimum_source_port" : "tcp_port_min",
        "maximum_source_port" : "tcp_port_max",
        "inter_packet_gap" : "llm_hdr_gap",
        "inter_packet_delay" : "inter_packet_delay",
        "ip_fragment_time" : "tcp_ipfrag_time",
        "fin_timeout" : "tcp_fin_timeout",
        "syn_retries" : "tcp_syn_retries",
        "synack_retries" : "tcp_synack_retries",
        "retansmit_retries1" : "tcp_retries1",
        "retransmit_retries2" : "tcp_retries2",
        "packet_reordering" : "tcp_reordering",
        "delayed_acks_segments" : "delayed_acks_segments",
        "delayed_acks_timeout" : "delayed_acks_timeout",
        "port_randomization" : "udp_port_randomization",
        "disable_path_mtu" : "ip_no_pmtu_disc",
        "window_scaling" : "tcp_window_scaling",
        "selective_ack" : "tcp_sack",
        "time_wait_reuse": "tcp_tw_reuse" ,
        "time_wait_recycle" : "tcp_tw_recycle",
        "time_wait_rfc1323_strict" : "tcp_tw_rfc1323_strict",
        "packet_timestamps" : "tcp_timestamps",
        "explicit_congestion_notification" : "tcp_ecn",
        #"source_port" : "",
        #"destination_port" : "",
        "bic" : "tcp_bic",
        "vegas_alpha": "tcp_vegas_alpha",
        "rfc1337": "tcp_rfc1337",
        "mem_low": "tcp_mem_low",
        "maximum_wmem": "tcp_wmem_max",
        "westwood" : "tcp_westwood",
        "avoid_vegas_congestion" : "tcp_vegas_cong_avoid",
        "maximum_rmem" : "tcp_rmem_max",
        "orphan_retries" : "tcp_orphan_retries",
        "maximum_time_wait_buckets" : "tcp_max_tw_buckets",
        "low_latency" : "tcp_low_latency",
        "minimum_rmem" : "tcp_rmem_min",
        "window_scale" : "tcp_adv_win_scale",
        #"wmem_default" : "tcp_wmem_default",
        "minimum_wmem" : "tcp_wmem_min",
        "stdurg" : "tcp_stdurg",
        "maximum_syn_backlog": "tcp_max_syn_backlog",
        "dsack" : "tcp_dsack",
        "abort_on_overflow": "tcp_abort_on_overflow",
        "fragment_reassembly_timer": "tcp_frto",
        "vegas_beta" : "tcp_vegas_beta",
        "maximum_orphans" : "tcp_max_orphans",
        "mem_pressure" : "tcp_mem_pressure",
        "moderate_receive_buffer" : "tcp_moderate_rcvbuf",
        "no_metrics_save" : "tcp_no_metrics_save",
        "retrans_collapse" : "tcp_retrans_collapse",
        #"rmem_default" : "tcp_rmem_default",
        "mem_high": "tcp_mem_high",
        "vegas_gamma" : "tcp_vegas_gamma",
        "fack": "tcp_fack",
        #"tcp_bic_fast_convergence": "",
        "bic_low_window": "tcp_bic_low_window",
        "app_win": "tcp_app_win",
        "keep_alive_probes" : "tcp_keepalive_probes"
    }
    
        
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """
        """
        self._devices_config = self._api._l47config.devices
        with Timer(self._api, "Tcp Configurations"):
            self._update_tcp()
    
    def _update_tcp(self):
        """Add any scenarios to the api server that do not already exist
        """
        
        for device in self._devices_config:
            self._update_tcp_config(device)
            
    def _update_tcp_config(self, device):
        """Add any scenarios to the api server that do not already exist
        """
        for tcp in device.tcps:
            url = self._api._config_url.get(tcp.ip_interface_name)
            url = self.get_community_url(url)
            tcp_child_url = "%snetwork/globalPlugins" % url
            response_list = self._api._request('GET', tcp_child_url)
            
            for index in range(len(response_list)):
                if response_list[index]['itemType'] == 'TCPPlugin':
                    tcp_url = "%s/%s" % (tcp_child_url, response_list[index]['objectID'])
                    self._api.logger.info("tcp_url:%s" % (tcp_url))
                    payload = self._api._set_payload(tcp, tcp_config._TCP_EN)
                    response = self._api._request('PATCH', tcp_url, payload)
                    payload = self._api._set_payload(tcp, tcp_config._TCP)
                    response = self._api._request('PATCH', tcp_url, payload)
                    self._api._config_url[tcp.name] = tcp_url
            
