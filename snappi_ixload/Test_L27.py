import sys
import logging as log
import pytest
sys.path.append("C:\\Users\\waseebai\\Documents\\GitHub\\snappi\\artifacts\\snappi")
import snappi
import time
import datetime
#from table import table

def test_snappi(request):

    api = snappi.api(location="https://10.39.71.237:443", ext='ixnetwork')
    # new config
    config = api.config()
    # port location is chassis-ip;card-id;port-id
    tx, rx = (
        config.ports
        .port(name='p1', location="10.39.64.169;2;1")
        .port(name='p2', location="10.39.64.169;2;2")
    )
    config.options.port_options.location_preemption = True
    # configure layer 1 properties
    ly, = config.layer1.layer1(name='ly')
    ly.port_names = [tx.name, rx.name]
    ly.speed = ly.SPEED_10_GBPS
    ly.media = ly.FIBER
    # configure flow properties
    flw, = config.flows.flow(name='flw')
    # flow endpoints
    flw.tx_rx.port.tx_name = tx.name
    flw.tx_rx.port.rx_name = rx.name
    # enable flow metrics
    flw.metrics.enable = True
    # configure rate, size, frame count
    flw.size.fixed = 128
    flw.rate.pps = 1000
    flw.duration.fixed_packets.packets = 10000
    # configure protocol headers with defaults fields
    flw.packet.ethernet().vlan().ipv4().tcp()
    # push configuration
    api.set_config(config)
    print("L23 config completed")

def test_snappi_load():
    print("Working on L47 Config")
    api = snappi.api(location="http://127.0.0.1:5000", verify=False)

    config = api.config()

    port_1 = config.ports.port(name="p1", location="10.39.46.4/11/3")[-1]
    port_2 = config.ports.port(name="p2", location="10.39.46.4/11/7")[-1]

    (d1, d2) = config.devices.device(name="d1").device(name="d2")
    (e1,) = d1.ethernets.ethernet(name="d1.e1")
    e1.connection.port_name = "p1"
    e1.mac = "00:00:01:00:00:01"
    (e2,) = d2.ethernets.ethernet(name="d2.e2")
    e2.connection.port_name = "p2"
    e2.mac = "00:00:02:00:00:01"
    (ip1,) = e1.ipv4_addresses.ipv4(name="e1.ipv4")
    ip1.address = "173.173.173.10"
    ip1.gateway = "0.0.0.0"
    (ip2,) = e2.ipv4_addresses.ipv4(name="e2.ipv4")
    ip2.address = "173.173.173.20"
    ip2.gateway = "0.0.0.0"

    (a1, a2) = config.apps.app(name="a1").app(name="a2")
    (t1,) = a1.tcp.tcp(name="tcp1")
    t1.keep_alive_time = 120
    (t2,) = a2.tcp.tcp(name="tcp2")
    t2.keep_alive_time = 120

    (h1,) = a1.http_client.httpclient()
    h1.client.name="HTTP_client1"
    h1.client.transport_name = t1.name
    h1.client.command_timeout = 60
    h1.client.cookie_reject_probability = False
    (m1,) = h1.client.methods.get()
    m1.server = "server1"
    m1.page = "/64k.html"


    (h2,) = a2.http_server.httpserver()
    #h2.server.name="HTTP_server1"
    h2.server.name = "HTTP_server1"
    h2.server.transport_name = t2.name
    h2.server.http_port = 80

    #Traffic configs

    traffic = a1.stateful_flows.statefulflow()[-1]
    traffic.client.protocol = h1.client.name
    traffic_c_ep=traffic.client.endpoints.client()[-1]
    traffic_c_ep.ip_interface_name = ip1.name

    traffic_c_ep.ports.values = [1]

    traffic.server.protocol = h2.server.name  
    traffic_sl_ep = traffic.server.endpoints.server()[-1]
    traffic_sl_ep.dest.name = ip2.name
    traffic_sl_ep.ports.values = [1]
    response = api.set_config(config)
    print(response)
    print("********************************")
    response = api.get_config()
    print(response)
    print("********************************")



if __name__ == "__main__":
    pytest.main(["-s", __file__])