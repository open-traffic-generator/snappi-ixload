# snappi Extension for IxNetwork

[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Build](https://github.com/open-traffic-generator/snappi-ixnetwork/workflows/Build/badge.svg)](https://github.com/open-traffic-generator/snappi-ixnetwork/actions)
[![pypi](https://img.shields.io/pypi/v/snappi_ixnetwork.svg)](https://pypi.org/project/snappi_ixnetwork)
[![python](https://img.shields.io/pypi/pyversions/snappi_ixnetwork.svg)](https://pypi.python.org/pypi/snappi_ixnetwork)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/open-traffic-generator/snappi-ixnetwork.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/open-traffic-generator/snappi-ixnetwork/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/open-traffic-generator/snappi-ixnetwork.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/open-traffic-generator/snappi-ixnetwork/context:python)
[![downloads](https://pepy.tech/badge/snappi-ixnetwork)](https://pepy.tech/project/snappi-ixnetwork)

This extension allows executing test scripts written using [snappi](https://github.com/open-traffic-generator/snappi) against  
IxLoad, (one of) Keysight's implementation of [Open Traffic Generator](https://github.com/open-traffic-generator/models/releases).

> The repository is under active development.

To start contributing, please see [contributing.md](contributing.md).

## Install on a client 

```sh
python -m pip install --upgrade "snappi[ixload]"
```

## Start scripting

```python
"""
Configure a raw TCP flow with,
- tx port as source to rx port as destination
- frame count 10000, each of size 128 bytes
- transmit rate of 1000 packets per second
Validate,
- frames transmitted and received for configured flow is as expected
"""

import snappi
# host is IxNetwork API Server
api = snappi.api(location='https://localhost:443', ext='ixnetwork')
# new config
config = api.config()
# port location is chassis-ip;card-id;port-id
tx, rx = (
    config.ports
    .port(name='tx', location='192.168.0.1;2;1')
    .port(name='rx', location='192.168.0.1;2;2')
)
# configure layer 1 properties
(d1, d2) = config.devices.device(name="d1").device(name="d2")
(e1,) = d1.ethernets.ethernet(name="d1.e1")
e1.connection.port_name = "p1"
e1.mac = "70:9C:91:69:00:00"
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

(t1,) = d1.tcps.tcp(name="Tcp1")
t1.ip_interface_name = ip1.name
t1.adjust_tcp_buffers = False
t1.keep_alive_time = 7000

(t2,) = d2.tcps.tcp(name="Tcp2")
t2.ip_interface_name = ip2.name
t2.time_wait_recycle = False
t2.time_wait_rfc1323_strict = True
t2.keep_alive_time = 600

(http_1,) = d1.https.http(name="HTTP1")
http_1.tcp_name = t1.name   #UDP configs can be mapped http.transport = udp_1.name
http_1.enable_tos = False
http_1.priority_flow_control_class = "v10"
(http_client,) = http_1.clients.client()
http_client.cookie_jar_size = 100
http_client.version = "1"

(http_2,) = d2.https.http(name="HTTP2")
http_2.tcp_name = t2.name		#UDP configs can be mapped http.transport = udp_2.name
http_2.enable_tos = False
http_2.priority_flow_control_class = "v10"
(http_server,) = http_2.servers.server()
http_server.rst_timeout = 100
http_server.enable_http2 = False
http_server.port = 80

(get_a,) = http_client.methods.method().method()
(get1,) = get_a.get.get()
get1.destination = "Traffic2_HTTPServer1:80" 
get1.page = "./1b.html"
# push configuration
api.set_config(config)
# start traffic 

cs = api.control_state()
cs.app.state = 'start' #cs.app.state.START 
response1 = api.set_control_state(cs) 
print(response1)
cs.app.state = 'stop' #cs.app.state.START 
api.set_control_state(cs) 
```