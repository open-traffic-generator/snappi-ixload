port_5 = config.ports.port(name="p5", location="10.39.46.4/11/5")[-1]
port_6 = config.ports.port(name="p6", location="10.39.46.4/11/6")[-1]
(device_5, device_6) = config.devices.device(name="device_5").device(name="device_6")
(eth_5,) = device_5.ethernets.ethernet(name="device_5.eth_5")
eth_5.connection.port_name = "p1"
eth_5.mac = "00:00:01:00:00:01"
(eth_6,) = device_6.ethernets.ethernet(name="device_6.eth_6")
eth_6.connection.port_name = "p2"
eth_6.mac = "00:00:02:00:00:01"
(ipv4_5,) = eth_5.ipv4_addresses.ipv4(name="eth_5.ipv4")
ipv4_5.address = "173.173.173.10"
ipv4_5.gateway = "0.0.0.0"
(ipv4_6,) = eth_6.ipv4_addresses.ipv4(name="eth_6.ipv4")
ipv4_6.address = "173.173.173.20"
ipv4_6.gateway = "0.0.0.0"

(app_3, app_4) = config.apps.app(name="app_3").app(name="app_4")
(tcp_3,) = app_3.tcp.tcp(name="tcp1")
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
response = api.set_config(config)
response = api.get_config()
