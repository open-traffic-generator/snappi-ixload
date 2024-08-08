api = snappi.api(location="http://127.0.0.1:5000", verify=False)

config = api.config()

port_1 = config.ports.port(name="p1", location="10.39.46.4/11/3")[-1]
port_2 = config.ports.port(name="p2", location="10.39.46.4/11/7")[-1]
(device_3, device_4) = config.devices.device(name="device_3").device(name="device_4")
(eth_3,) = device_3.ethernets.ethernet(name="device_3.eth_3")
eth_3.connection.port_name = "p1"
eth_3.mac = "00:00:01:00:00:01"
(eth_4,) = device_4.ethernets.ethernet(name="device_4.eth_4")
eth_4.connection.port_name = "p2"
eth_4.mac = "00:00:02:00:00:01"
(ipv4_3,) = eth_3.ipv4_addresses.ipv4(name="eth_3.ipv4")
ipv4_3.address = "173.173.173.10"
ipv4_3.gateway = "0.0.0.0"
(ipv4_4,) = eth_4.ipv4_addresses.ipv4(name="eth_4.ipv4")
ipv4_4.address = "173.173.173.20"
ipv4_4.gateway = "0.0.0.0"

(app_1, app_2) = config.apps.app(name="app_1").app(name="app_2")
(tcp_1,) = app_1.tcp.tcp(name="tcp1")
tcp_1.keep_alive_time = 120
(tcp2,) = app_2.tcp.tcp(name="tcp2")
tcp2.keep_alive_time = 120

(http_client_1,) = app_1.http_client.httpclient()
http_client_1.client.name="HTTP_client1"
http_client_1.client.transport_name = tcp_1.name
http_client_1.client.command_timeout = 60
http_client_1.client.cookie_reject_probability = False
(m1,) = http_client_1.client.methods.get()
m1.server = "Traffic2_HTTPServer1:80"
m1.page = "/64k.html"


(http_client_2,) = app_2.http_server.httpserver()
#http_client_2.server.name="HTTP_server1"
http_client_2.server.name = "HTTP_server1"
http_client_2.server.transport_name = tcp2.name
http_client_2.server.http_port = 80

#Traffic configs

traffic = app_1.stateful_flows.statefulflow()[-1]
traffic.client.protocol = http_client_1.client.name
traffic_c_ep=traffic.client.endpoints.client()[-1]
traffic_c_ep.ip_interface_name = ipv4_3.name

traffic_c_ep.ports.values = [1]

traffic.server.protocol = http_client_2.server.name  
traffic_sl_ep = traffic.server.endpoints.server()[-1]
traffic_sl_ep.dest.name = ipv4_4.name
traffic_sl_ep.ports.values = [1]

#Testcase for tcp as endpoints

port_5 = config.ports.port(name="p5", location="10.39.46.4/11/5")[-1]
port_6 = config.ports.port(name="p6", location="10.39.46.4/11/6")[-1]
(device_5, device_6) = config.devices.device(name="device_5").device(name="device_6")
(eth_5,) = device_5.ethernets.ethernet(name="device_5.eth_5")
eth_5.connection.port_name = "p5"
eth_5.mac = "00:00:01:00:00:01"
(eth_6,) = device_6.ethernets.ethernet(name="device_6.eth_6")
eth_6.connection.port_name = "p6"
eth_6.mac = "00:00:02:00:00:01"
(ipv4_5,) = eth_5.ipv4_addresses.ipv4(name="eth_5.ipv4")
ipv4_5.address = "173.173.173.10"
ipv4_5.gateway = "0.0.0.0"
(ipv4_6,) = eth_6.ipv4_addresses.ipv4(name="eth_6.ipv4")
ipv4_6.address = "173.173.173.20"
ipv4_6.gateway = "0.0.0.0"

(app_3, app_4) = config.apps.app(name="app_3").app(name="app_4")
(tcp_3,) = app_3.tcp.tcp(name="tcp_3")
tcp_3.keep_alive_time = 120
(tcp_4,) = app_4.tcp.tcp(name="tcp_4")
tcp_4.keep_alive_time = 120


#stateful_2 configs

stateful_2 = app_3.stateful_flows.statefulflow()[-1]
stateful_2.client.protocol = tcp_3.name
stateful_2_c_ep=stateful_2.client.endpoints.client()[-1]
stateful_2_c_ep.ip_interface_name = ipv4_5.name

stateful_2_c_ep.ports.values = [1]

stateful_2.server.protocol = tcp_4.name
stateful_2_sl_ep = stateful_2.server.endpoints.server()[-1]
stateful_2_sl_ep.dest.name = ipv4_6.name
stateful_2_sl_ep.ports.values = [1]

# Testcase for One arm test

port_1 = config.ports.port(name="p7", location="10.39.46.4/11/7")[-1]
(device_7,)= config.devices.device(name="device_7")
(eth_7,) = device_7.ethernets.ethernet(name="device_7.eth_7")
eth_7.connection.port_name = "p7"
eth_7.mac = "00:00:01:00:00:01"
(ipv4_7,) = eth_7.ipv4_addresses.ipv4(name="eth_7.ipv4")
ipv4_7.address = "173.173.173.10"
ipv4_7.gateway = "0.0.0.0"

(app_5,)  = config.apps.app(name="app_5")
(tcp_5,) = app_5.tcp.tcp(name="tcp_5")
tcp_5.keep_alive_time = 120

(http_client_1,) = app_5.http_client.httpclient()
http_client_1.client.name="HTTP_client1"
http_client_1.client.transport_name = tcp_5.name
http_client_1.client.command_timeout = 60
http_client_1.client.cookie_reject_probability = False
(m1,) = http_client_1.client.methods.get()
m1.server = "10.10.10.100"
m1.page = "/64k.html"

#stateful_3 configs
traffic = app_5.stateful_flows.statefulflow()[-1]
traffic.client.protocol = http_client_1.client.name
traffic_c_ep=traffic.client.endpoints.client()[-1]
traffic_c_ep.ip_interface_name = ipv4_7.name
traffic_c_ep.ports.values = [1]

traffic_sl_ep = traffic.server.endpoints.server()[-1]
traffic_sl_ep.dest.ipv4_address = "10.10.10.100"

response = api.set_config(config)
print(response)

response = api.get_config()
print(response)