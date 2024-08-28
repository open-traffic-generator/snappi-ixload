import sys
#sys.path.append("C:\\Users\\waseebai\\Documents\\GitHub\\snappi\\artifacts\\snappi")
#sys.path.insert(0, "c:\\Users\\waseebai\\Documents\\project\\snappi_l47\\snappi\\artifacts\\snappi")

import snappi

api = snappi.api(location="http://127.0.0.1:5000", verify=False)
config = api.config()

port_1 = config.ports.port(name="p1", location="amit.buh.is.keysight.com/1/1")[-1]
port_2 = config.ports.port(name="p2", location="amit.buh.is.keysight.com/1/2")[-1]

(d1, d2) = config.devices.device(name="d1").device(name="d2")
(e1,) = d1.ethernets.ethernet(name="d1.e1")
#(e1,e3) = d1.ethernets.ethernet(name="d1.e1").ethernet(name="d1.e3")
e1.connection.port_name = "p1"
e1.mac = "70:9C:91:69:00:00"
e1.step = "00:00:00:00:00:01" 
e1.count = 1
#e3.mac = "00:00:01:00:00:03"
#e3.step = "00:00:00:00:00:01" 
#e3.count = 1

(e2,) = d2.ethernets.ethernet(name="d2.e2")
e2.connection.port_name = "p2"
e2.mac = "7C:5D:68:26:00:00"

(vlan1,) = e1.vlans.vlan(name = "vlan1")
vlan1.id = 1
vlan1.priority = 1
vlan1.tpid = "x8100"
#(vlan3,) = e3.vlans.vlan(name = "vlan3")
#vlan3.id = 1
#vlan3.priority = 1
#vlan3.tpid = "x8100"
(vlan2,) = e2.vlans.vlan(name = "vlan2")
vlan2.id = 1
vlan2.priority = 1
vlan2.tpid = "x8100"
(ip1,) = e1.ipv4_addresses.ipv4(name="e1.ipv4")
ip1.address = "173.173.173.10"
ip1.gateway = "0.0.0.0"
ip1.step = "0.0.0.1"
ip1.count = 1
#(ip3,) = e3.ipv4_addresses.ipv4(name="e3.ipv4")
#ip3.address = "173.173.173.20"
#ip3.gateway = "0.0.0.0"
#ip3.step = "0.0.0.1"
#ip3.count = 1
(ip2,) = e2.ipv4_addresses.ipv4(name="e2.ipv4")
ip2.address = "173.173.173.30"
ip2.gateway = "0.0.0.0"



#TCP/UDP configs

(t1,) = d1.tcps.tcp(name="Tcp1")
t1.ip_interface_name = ip1.name
t1.adjust_tcp_buffers = False
t1.keep_alive_time = 7000
t1.keep_alive_interval = 60
t1.receive_buffer_size = 8062
t1.transmit_buffer_size = 8062
t1.retransmission_minimum_timeout = 180
t1.retransmission_maximum_timeout = 1000
t1.minimum_source_port = 80
t1.maximum_source_port = 1024
t1.inter_packet_gap = 9
t1.inter_packet_delay = 1
t1.ip_fragment_time = 1
t1.fin_timeout = 60
t1.syn_retries = 5
t1.synack_retries = 5
t1.retansmit_retries1 = 3
t1.retransmit_retries2 = 3
t1.packet_reordering = 3
t1.delayed_acks_segments = 0
t1.delayed_acks_timeout = 0
t1.port_randomization = False
t1.disable_path_mtu = False
t1.window_scaling = False
t1.selective_ack = False
t1.time_wait_reuse = False
t1.time_wait_recycle = False
t1.time_wait_rfc1323_strict = False
t1.packet_timestamps = False
t1.explicit_congestion_notification  = False
t1.bic = 0
t1.vegas_alpha = 2
t1.rfc1337 = True
t1.mem_low = 24756
t1.maximum_wmem = 262144
t1.westwood = 0
t1.avoid_vegas_congestion = 0
t1.maximum_rmem = 262144
t1.orphan_retries = 0
t1.maximum_time_wait_buckets = 1800
t1.low_latency = 0
t1.minimum_rmem = 4096
t1.window_scale = 2
t1.minimum_wmem = 4096
t1.stdurg = False
t1.maximum_syn_backlog = 1024
t1.dsack = True
t1.abort_on_overflow = True
t1.fragment_reassembly_timer = 0
t1.vegas_beta = 6
t1.maximum_orphans = 8192
t1.mem_pressure = 32768
t1.moderate_receive_buffer = 0
t1.no_metrics_save = True
t1.retrans_collapse = True
t1.mem_high = 49152
t1.vegas_gamma = 2
t1.fack = True
t1.bic_low_window = 14
t1.app_win = 31
t1.keep_alive_probes = 9






# t1.rmem_default = 65536
# t1.transmit_buffer_size = 65536
# t1.time_wait_recycle = False
# t1.time_wait_rfc1323_strict = True
# t1.keep_alive_time = 600

(t2,) = d2.tcps.tcp(name="Tcp2")
t2.ip_interface_name = ip2.name
t2.time_wait_recycle = False
t2.time_wait_rfc1323_strict = True
t2.keep_alive_time = 600
(http_1,) = d1.https.http(name="HTTP1")
http_1.tcp_name = t1.name   #UDP configs can be mapped http.transport = udp_1.name
http_1.enable_tos = False
http_1.priority_flow_control_class = "v10"
http_1.precedence_tos = "v20"
http_1.delay_tos = "v10"
http_1.throughput_tos = "v10"
http_1.url_stats_count = 10
http_1.disable_priority_flow_control =  0
http_1.enable_vlan_priority = False
http_1.vlan_priority = 0
http_1.esm = 1460
http_1.enable_esm =  False
http_1.time_to_live_value = 64
http_1.tcp_close_option = "v10"
http_1.enable_integrity_check_support = False
http_1.type_of_service = 0
http_1.high_perf_with_simulated_user =  False
(http_client,) = http_1.clients.client()
http_client.cookie_jar_size = 100
http_client.version = "1"
http_client.cookie_reject_probability = True
http_client.enable_cookie_support = False
http_client.command_timeout = 600
http_client.command_timeout_ms = 0
http_client.enable_proxy = False
http_client.keep_alive = False
http_client.max_sessions = 3
http_client.max_streams = 1
http_client.max_pipeline = 1
http_client.max_persistent_requests = 1
http_client.exact_transactions = 0
http_client.follow_http_redirects = False
http_client.enable_decompress_support = False
http_client.enable_per_conn_cookie_support = False
http_client.ip_preference = "v10"
http_client.enable_large_header = False
http_client.max_header_len = 1024
http_client.per_header_percent_dist =  False
http_client.enable_auth = False
http_client.piggy_back_ack = True
http_client.tcp_fast_open = False
http_client.content_length_deviation_tolerance = 0
http_client.disable_dns_resolution_cache = False
http_client.enable_consecutive_ips_per_session = False
http_client.enable_achieve_cc_first = False
http_client.enable_traffic_distribution_for_cc = False
http_client.browser_emulation_name = "Browser1"

#http_1.client(endpoints_allow_inbound)

# get1 = http1.client.methods.add("get")
# get1.page = "./1b.html"
# get1.destination = "10.0.10.1" #real http server ip or emulated http object  get1.destination = "http2:80"
#for http server emulation
#get1.destination = http_2.name 
(http_2,) = d2.https.http(name="HTTP2")
http_2.tcp_name = t2.name		#UDP configs can be mapped http.transport = udp_2.name
http_2.enable_tos = False
http_2.priority_flow_control_class = "v10"
http_2.precedence_tos = "v20"
http_2.delay_tos = "v10"
http_2.throughput_tos = "v10"
http_2.url_stats_count = 10
http_2.disable_priority_flow_control = 0
http_2.enable_vlan_priority = False
http_2.vlan_priority = 0
http_2.esm = 1460
http_2.enable_esm = False 
http_2.time_to_live_value = 64
http_2.tcp_close_option = "v10"
http_2.enable_integrity_check_support = False
http_2.type_of_service = 0 
http_2.high_perf_with_simulated_user = False		#UDP configs can be mapped http.transport = udp_2.name
#http_2.server(endpoints_allow_outbound)
(http_server,) = http_2.servers.server()
http_server.rst_timeout = 100
http_server.enable_http2 = False
http_server.port = 80
http_server.request_timeout = 300
http_server.maximum_response_delay = 0
http_server.minimum_response_delay = 0
http_server.dont_expect_upgrade = False
http_server.enable_per_server_per_url_stat = False
http_server.url_page_size = 1024
http_server.enable_chunk_encoding = False
http_server.enable_md5_checksum = False

(get_a,delete_a) = http_client.methods.method().method()
(get1,) = get_a.get.get()
get1.destination = "Traffic2_HTTPServer1:80" 
get1.page = "./1b.html"
#get1.destination = "Traffic2_HTTPServer1:80" #real http server ip or emulated http object  get1.destination = "http2:80"
#for http server emulation
#get1.destination = http_2.name   
# (post1,) = post1_a.post.post()
# post1.destination = "Traffic2_HTTPServer1:80" 
# post1.page = "./1b.html"
(delete1,) = delete_a.delete.delete()
delete1.destination = "Traffic2_HTTPServer1:80" 
delete1.page = "./1b.html"

tp = config.trafficprofile.trafficprofile()
#tp[0].objective_type = ["simulated_user", "throughput_kbps", "throughput_mbps", "concurrent_connections", "connection_per_sec", "transactions_per_sec","connection_attempts_per_sec"]
tp[0].objective_type = ["throughput_mbps"]
tp[0].objective_value = [102]
tp[0].timeline = ['Timeline1']

obj_type = tp[0].objectives.objective()
# obj_type[0].throughput_kbps.enable_controlled_user_adjustment = True
# obj_type[0].throughput_kbps.sustain_time=5
# obj_type[0].throughput_kbps.ramp_down_time = 10
# obj_type[0].simulated_user.ramp_up_value = 15
# obj_type[0].simulated_user.sustain_time = 5
# obj_type[0].simulated_user.ramp_down_time =11
# obj_type[0].simulated_user.enable_controlled_user_adjustment = True
# obj_type[0].concurrent_connections.enable_controlled_user_adjustment = True
# obj_type[0].concurrent_connections.sustain_time=6
# obj_type[0].concurrent_connections.ramp_down_time=12
# obj_type[0].concurrent_connections.ramp_down_value=10
# obj_type[0].connection_per_sec.enable_controlled_user_adjustment = True
# obj_type[0].connection_per_sec.sustain_time=14
# obj_type[0].connection_per_sec.ramp_down_time=12
# obj_type[0].transactions_per_sec.enable_controlled_user_adjustment = True
# obj_type[0].transactions_per_sec.sustain_time=10
# obj_type[0].transactions_per_sec.ramp_down_time=11
# obj_type[0].connection_attempts_per_sec.enable_controlled_user_adjustment = True
# obj_type[0].connection_attempts_per_sec.sustain_time=12
# obj_type[0].connection_attempts_per_sec.ramp_down_time=13
obj_type[0].throughput_mbps.enable_controlled_user_adjustment = True
obj_type[0].throughput_mbps.sustain_time=6
obj_type[0].throughput_mbps.ramp_down_time = 11


(segment1,segment2) = tp[0].segment.segment().segment()
segment1.name = "Linear segment1"
segment1.start = 0
segment1.duration = 10
segment1.rate = 10
segment1.target = 100

# obj_type = tp[0].objectives.objective()
# obj_type[0].simulated_user.ramp_up_value = 15
# obj_type[0].simulated_user.sustain_time = 5
# obj_type[0].simulated_user.ramp_down_time =11
# obj_type[0].throughput_kbps.enable_controlled_user_adjustment = True
# obj_type[0].throughput_kbps.sustain_time=5
# obj_type[0].throughput_kbps.ramp_down_time = 10
# obj_type[0].throughput_mbps.enable_controlled_user_adjustment = True
# obj_type[0].throughput_mbps.sustain_time=6
# obj_type[0].throughput_mbps.ramp_down_time = 11
# obj_type[0].concurrent_connections.enable_controlled_user_adjustment = True
# obj_type[0].concurrent_connections.sustain_time=6
# obj_type[0].concurrent_connections.ramp_down_time=12
# obj_type[0].concurrent_connections.ramp_down_value=13
# obj_type[0].connection_per_sec.enable_controlled_user_adjustment = True
# obj_type[0].connection_per_sec.sustain_time=14
# obj_type[0].connection_per_sec.ramp_down_time=12
#obj_type[0].connection_per_sec.ramp_down_value=15



response = api.set_config(config)
print(response)

#cs = api.control_state()
#cs.app.state = 'start' #cs.app.state.START 
#response1 = api.set_control_state(cs) 
#print(response1)
#cs.app.state = 'stop' #cs.app.state.START 
#api.set_control_state(cs)            




