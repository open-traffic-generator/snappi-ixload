import sys
#sys.path.insert(0, "C:\\Users\\waseebai\\Documents\\project\\GitHub\\snappi\\artifacts\\snappi")
import snappi
import time

api = snappi.api(location="localhost:8080", ext="ixload", verify=False, version="10.00.0.152")
config = api.config()

port_1 = config.ports.port(name="p1", location="10.39.65.156/2/11")[-1]
port_2 = config.ports.port(name="p2", location="10.39.65.156/2/12")[-1]
#port_1 = config.ports.port(name="p1", location="10.39.65.156/2/1")[-1]
#port_2 = config.ports.port(name="p2", location="10.39.65.156/2/2")[-1]

(d1, d2,) = config.devices.device(name="d1").device(name="d2")
(e1,) = d1.ethernets.ethernet(name="d1.e1")
e1.connection.port_name = "p1"
e1.mac = "70:9C:91:69:00:00"
e1.step = "00:00:00:00:00:01" 
e1.count = 1
(e2,) = d2.ethernets.ethernet(name="d2.e2")
e2.connection.port_name = "p2"
e2.mac = "7C:5D:68:26:00:00"

(ip1,) = e1.ipv4_addresses.ipv4(name="e1.ipv4")
ip1.address = "173.173.173.10"
ip1.gateway = "0.0.0.0"
ip1.step = "0.0.0.1"
ip1.count = 1
(ip2,) = e2.ipv4_addresses.ipv4(name="e2.ipv4")
ip2.address = "173.173.173.30"
ip2.gateway = "0.0.0.0"

(vlan1,) = e1.vlans.vlan(name = "vlan1")
vlan1.id = 1
vlan1.priority = 1
vlan1.tpid = 'x9100'
(vlan2,) = e2.vlans.vlan(name = "vlan2")
vlan2.id = 1
vlan2.priority = 1
vlan2.tpid = 'x9100'

#TCP/UDP configs
(t1,) = d1.tcps.tcp(name="Tcp1")
t1.ip_interface_name = ip1.name
t1.adjust_tcp_buffers = False
t1.keep_alive_time = 7000
t1.keep_alive_interval = 60
t1.receive_buffer_size = 1024
t1.transmit_buffer_size = 1024


(t2,) = d2.tcps.tcp(name="Tcp2")
t2.ip_interface_name = ip2.name
t2.time_wait_recycle = False
t2.time_wait_rfc1323_strict = True
t2.keep_alive_time = 600
(http_1,) = d1.https.http(name="HTTP1")
http_1.tcp_name = t1.name   #UDP configs can be mapped http.transport = udp_1.name
http_1.high_perf_with_simulated_user =  False
(http_client,) = http_1.clients.client()
http_client.name = "Http1Client1"
http_client.cookie_jar_size = 100
http_client.version = "1"
http_client.cookie_reject_probability = True
http_client.enable_cookie_support = False

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

http_2.high_perf_with_simulated_user = False		#UDP configs can be mapped http.transport = udp_2.name

(http_server,) = http_2.servers.server()
http_server.name = "Http1Server1"
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

(get_a, delete_a) = http_client.methods.method().method()
(get1,) = get_a.get.get()
get1.destination = "Traffic2_Http1Server1:80" 
get1.page = "./1b.html"
get1.name_value_args =""
(delete1,) = delete_a.delete.delete()
delete1.destination = "Traffic2_Http1Server1:80"
delete1.page = "./1b.html"

tp = config.trafficprofile.trafficprofile()
#For Http1Client1 
tp[0].app = [http_client.name, http_server.name]
tp[0].objective_type = ["connection_per_sec", "simulated_user"]
tp[0].objective_value = [60, 80]
tp[0].timeline = ['Timeline1']
obj_type = tp[0].objectives.objective()
obj_type[0].connection_per_sec.enable_controlled_user_adjustment = True
obj_type[0].connection_per_sec.sustain_time=14
obj_type[0].connection_per_sec.ramp_down_time=12
obj_type[0].connection_per_sec.time_to_first_iter = 3
obj_type[0].connection_per_sec.iteration = 4

tm1=tp[0].trafficmap.trafficmap()
tm1[0].port_map_policy_name  = "custom"
cust1 = tm1[0].custom.custom()
cust1[0].name = "samplemap"
mt1 = cust1[0].mapping_type
mt1.vlan_range_pairs.enable =True
mt1.vlan_range_pairs.destination_id = 1

response = api.set_config(config)
print(response)
# payload = {"mtu": "1400"}
# url = "ixload/test/activeTest/communityList/0/network/stack/childrenList/2/macRangeList"
# res = api.ixload_configure("patch", url, payload)

# payload = {"itemType": "L2EthernetPlugin"}
# url = "ixload/test/activeTest/communityList/0/network/stack/childrenList"
# res = api.ixload_configure("post", url, payload)


cs = api.control_state()
cs.app.state = 'start'  # cs.app.state.START
response1 = api.set_control_state(cs)
print(response1)
time.sleep(30)
req = api.metrics_request()

req.choice= "httpclient"
req.httpclient.stat_name = ["TCP Connections Established",
                            "HTTP Bytes Received"]
req.httpclient.end_test = False
res = api.get_metrics(req).httpclient_metrics
print(res)
print("*******************************************")
req1 = api.metrics_request()
req1.choice= "httpserver"
req1.httpserver.end_test = False
req1.httpserver.stat_name = ["Transmitted Data Rate (Kbps)"]
res1 = api.get_metrics(req1).httpserver_metrics
print(res1)
print("*******************************************")


cs.app.state = 'stop'  # cs.app.state.START
api.set_control_state(cs)