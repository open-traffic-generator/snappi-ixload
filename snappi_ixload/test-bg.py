import sys


#sys.path.insert(0, "C:\\Users\\waseebai\\Documents\\project\\GitHub\\snappi\\artifacts\\snappi")
import snappi


import ipaddress
import os

import macaddress

ipp = ipaddress.ip_address
maca = macaddress.MAC

ENI_START = 1
ENI_COUNT = 5# 64
ENI_MAC_STEP = '00:00:00:18:00:00'
ENI_STEP = 1
ENI_L2R_STEP = 1000

PAL = ipp("221.1.0.1")
PAR = ipp("221.2.0.1")

ACL_TABLE_MAC_STEP = '00:00:00:02:00:00'
ACL_POLICY_MAC_STEP = '00:00:00:00:00:32'

ACL_RULES_NSG = 1000  # 1000
ACL_TABLE_COUNT = 5

IP_PER_ACL_RULE = 25  # 128
IP_MAPPED_PER_ACL_RULE = IP_PER_ACL_RULE # 40
IP_ROUTE_DIVIDER_PER_ACL_RULE = 64 # 8, must be a power of 2 number

IP_STEP1 = int(ipp('0.0.0.1'))
#IP_STEP2 = int(ipp('0.0.1.0'))
#IP_STEP3 = int(ipp('0.1.0.0'))
#IP_STEP4 = int(ipp('1.0.0.0'))
IP_STEP_ENI = int(ipp('0.64.0.0')) # IP_STEP4
IP_STEP_NSG = int(ipp('0.2.0.0')) # IP_STEP3 * 4
IP_STEP_ACL = int(ipp('0.0.0.50')) # IP_STEP2 * 2
IP_STEPE = int(ipp('0.0.0.2'))


IP_L_START = ipaddress.ip_address('36.1.0.1')
IP_R_START = ipaddress.ip_address('36.1.100.1')

MAC_L_START = macaddress.MAC('00:1A:C5:00:00:01')
MAC_R_START = macaddress.MAC('00:1B:6E:00:00:01')


def build_node_ips(count, vpc, nodetype="client"):
    if nodetype in "client":
        ip = ipp(int(IP_R_START) + (IP_STEP_NSG * count) + int(ipp('0.0.64.0')) * (vpc - 1))
    if nodetype in "server":
        ip = ipp(int(IP_L_START) + int(ipp('0.0.64.0')) * (vpc - 1))

    return str(ip)


def build_node_macs(count, vpc, nodetype="client"):

    if nodetype in "client":
        #m = maca(int(MAC_R_START) + int(maca('00-00-00-30-00-00')) * (vpc - 1) + (int(maca(ACL_TABLE_MAC_STEP)) * count))
        m = maca(int(MAC_R_START) + int(maca('00-00-00-18-00-00')) * (vpc - 1) + (int(maca(ACL_TABLE_MAC_STEP)) * count))
    if nodetype in "server":
        #m = maca(int(MAC_L_START) + int(maca('00-00-00-30-00-00')) * (vpc - 1))
        m = maca(int(MAC_L_START) + int(maca('00-00-00-18-00-00')) * (vpc - 1))

    return str(m).replace('-', ':')


def build_node_vlan(index, nodetype="client"):

    hero_b2b = False

    """
    if index > 0:
        index = index + 1 * index
        #index = index + 1
    """

    if nodetype == 'client':
        vlan = ENI_L2R_STEP + index + 1
        #vlan = ENI_L2R_STEP + index
    else:
        ENI_STEP = 1
        if hero_b2b is True:
            vlan = 0
        else:
            vlan = ENI_STEP + index

    return vlan


def main():
    ####### Start Here ######
    api = snappi.api(location="http://127.0.0.1:5000", verify=False)
    config = api.config()

    #port_1 = config.ports.port(name="p1", location="10.36.78.43/2/1")[-1]
    #port_2 = config.ports.port(name="p2", location="10.36.78.43/2/2")[-1]

    port_1 = config.ports.port(name="p1", location="amit.buh.is.keysight.com/1/2")[-1]
    port_2 = config.ports.port(name="p2", location="amit.buh.is.keysight.com/2/2")[-1]

    # client/server IP ranges created here

    (d1, d2) = config.devices.device(name="d1").device(name="d2")

    for eni in range(ENI_COUNT):

        ####### client ######
        de_tmp = "d1.e1"
        d1.name = de_tmp

        # ethernet section
        eth = d1.ethernets.add()
        eth.name = "e1"
        eth.connection.port_name = "p1"
        eth.mac = build_node_macs(0, eni+1, nodetype="client")

        # ip section
        ip1 = eth.ipv4_addresses.ipv4()[-1]
        ip1.name = "{}.ipv4".format(eth.name)
        ip1.address = build_node_ips(0, eni+1, nodetype="client")
        ip1.prefix = 10
        ip1.gateway = "0.0.0.0"

        # vlan section
        vlan = eth.vlans.vlan()[-1]
        vlan.name = "{}.vlan".format(eth.name)
        vlan.id = build_node_vlan(eni, nodetype="client")
        vlan.priority = 1
        vlan.count = 1
        vlan.tpid = "x8100"


        ###### SERVER ######
        de_tmp_server = "d2.e2"
        d2.name = de_tmp_server

        # ethernet section
        eth2 = d2.ethernets.add()
        eth2.name = "e2"
        eth2.connection.port_name = "p2"
        eth2.mac = build_node_macs(0, eni+1, nodetype="server")

        # ip section
        ip2 = eth2.ipv4_addresses.ipv4()[-1]
        ip2.name = "{}.ipv4".format(eth2.name)
        ip2.address = build_node_ips(0, eni+1, nodetype="server")
        ip2.prefix = 10
        ip2.gateway = "0.0.0.0"

        # vlan section
        vlan2 = eth2.vlans.vlan()[-1]
        vlan2.name = "{}.vlan".format(eth2.name)
        vlan2.id = build_node_vlan(eni, nodetype="server")
        vlan2.priority = 1
        vlan2.count = 1
        vlan2.tpid = "x8100"

    eth.connection.port_name = "p1"
    eth2.connection.port_name = "p2"
    # tcp/http client settings
    (t1,) = d1.tcps.tcp(name="Tcp1")
    t1.ip_interface_name = ip1.name
    t1.adjust_tcp_buffers = False
    t1.receive_buffer_size = 1024
    t1.transmit_buffer_size = 1024
    t1.keep_alive_time = 7200
    t1.keep_alive_interval = 75
    t1.keep_alive_probes = 9
    t1.retransmission_minimum_timeout = 200
    t1.retransmission_maximum_timeout = 120000
    t1.minimum_source_port = 1024
    t1.maximum_source_port = 65530
    t1.inter_packet_gap = 8
    t1.inter_packet_delay = 0
    t1.ip_fragment_time = 30
    t1.fin_timeout = 60
    t1.syn_retries = 5
    t1.synack_retries = 5
    t1.retansmit_retries1 = 3
    t1.retransmit_retries2 = 5
    t1.packet_reordering = 3
    t1.delayed_acks_segments = 0
    t1.delayed_acks_timeout = 0
    t1.disable_path_mtu = True
    t1.window_scaling = False
    t1.selective_ack = True
    t1.time_wait_reuse = False
    t1.time_wait_recycle = True
    t1.time_wait_rfc1323_strict = False
    t1.packet_timestamps = True
    t1.explicit_congestion_notification = False
    t1.fragment_reassembly_timer = 30

    # http
    (http_1,) = d1.https.http(name="HTTP1")
    http_1.tcp_name = t1.name  # UDP configs can be mapped http.transport = udp_1.name
    http_1.url_stats_count = 10
    http_1.time_to_live_value = 64
    http_1.high_perf_with_simulated_user = False
    (http_client,) = http_1.clients.client()
    http_client.name = "http_client1"
    http_client.cookie_jar_size = 10
    http_client.version = "1"
    http_client.cookie_reject_probability = True
    http_client.enable_cookie_support = False
    http_client.command_timeout = 600
    http_client.command_timeout_ms = 0
    http_client.keep_alive = False
    http_client.max_persistent_requests = 0
    http_client.max_sessions = 1
    http_client.max_streams = 1
    http_client.max_pipeline = 1
    http_client.piggy_back_ack = True
    http_client.tcp_fast_open = False
    http_client.content_length_deviation_tolerance = 0

    (get_a, delete_a) = http_client.methods.method().method()
    (get1,) = get_a.get.get()
    #get1.destination = "Traffic2_HTTPServer1:80"
    get1.destination = "Traffic2_http_server1:80"
    get1.page = "./1b.html"
    # get1.destination = "Traffic2_HTTPServer1:80" #real http server ip or emulated http object  get1.destination = "http2:80"


    # tcp/http server settings
    # tcp
    (t2,) = d2.tcps.tcp(name="Tcp2")
    t2.ip_interface_name = ip2.name
    t2.adjust_tcp_buffers = False
    t2.receive_buffer_size = 1024
    t2.transmit_buffer_size = 1024
    t2.time_wait_recycle = False
    t2.time_wait_rfc1323_strict = True
    t2.keep_alive_time = 600

    # http
    (http_2,) = d2.https.http(name="HTTP2")
    http_2.tcp_name = t2.name  # UDP configs can be mapped http.transport = udp_2.name
    http_2.enable_tos = False
    http_2.url_stats_count = 10
    http_2.time_to_live_value = 64
    http_2.high_perf_with_simulated_user = False  # UDP configs can be mapped http.transport = udp_2.name
    (http_server,) = http_2.servers.server()
    http_server.name = "http_server1"
    http_server.rst_timeout = 100
    http_server.enable_http2 = False
    http_server.port = 80
    http_server.request_timeout = 5
    http_server.maximum_response_delay = 0
    http_server.minimum_response_delay = 0
    http_server.url_page_size = 1024

    ## Traffic Profile
    (tp1,) = config.trafficprofile.trafficprofile()
    # # # # # traffic_profile = config.TrafficProfiles.TrafficProfile(name = "traffic_profile_1")
    tp1.app = [http_client.name,
                   http_server.name]  # traffic_profile_cps.app - "app" using it for reference can be some generic name for traffic profile on which traffic has to flow
    tp1.objective_type = ["connection_per_sec", "simulated_user"]
    tp1.objective_value = [100, 120000]
    (obj_type,) = tp1.objectives.objective()
    obj_type.connection_per_sec.enable_controlled_user_adjustment = True
    obj_type.connection_per_sec.sustain_time=14
    obj_type.connection_per_sec.ramp_down_time=12
    obj_type.connection_per_sec.time_to_first_iter = 3
    obj_type.connection_per_sec.iteration = 4
    # (segment1, segment2) = tp1.segment.segment().segment()
    # segment1.name = "Linear segment1"
    # segment1.start = 0
    # segment1.duration = 10
    # segment1.rate = 10
    # segment1.target = 100
    # segment2.name = "Linear segment2"
    # segment2.start = 0
    # segment2.duration = 10
    # segment2.rate = 10
    # segment2.target = 100
    # tp1.timeline = [segment1.name, segment2.name]
    tp1.timeline = ['Timeline5']
    
    
    # ## Traffic Maps
    tm1 = tp1.trafficmap.trafficmap()
    tm1[0].port_map_policy_name  = "custom"
    cust1 = tm1[0].custom.custom()
    cust1[0].name = "vlanRangePairs"
    mt1 = cust1[0].mapping_type
    mt1.vlan_range_pairs.enable = True
    mt1.vlan_range_pairs.destination_id = 2

    ##### Set config
    response = api.set_config(config)
    print(response)

    cs = api.control_state()
    cs.app.state = 'start' #cs.app.state.START
    response1 = api.set_control_state(cs)
    print(response1)
    req = api.metrics_request()
    #HTTP client
    req.choice= "httpclient"
    #req.httpclient.stat_name = ["HTTP Simulated Users", "HTTP Concurrent Connections", "HTTP Connect Time (us)", "TCP Connections Established", "HTTP Bytes Received"]
    req.httpclient.all_stats = True # for  all stats 
    res = api.get_metrics(req).httpclient_metrics
    print(res)

    req1 = api.metrics_request()
    req1.choice= "httpserver"
    req1.httpserver.stat_name = ["TCP Connections in ESTABLISHED State", "TCP FIN Received","HTTP Bytes Received"]
    #req1.httpserver.all_stats=True # for all stats - True
    res1 = api.get_metrics(req1).httpserver_metrics
    print(res1)
    
    cs.app.state = 'stop' #cs.app.state.START
    api.set_control_state(cs)



if __name__ == '__main__':
    main()
