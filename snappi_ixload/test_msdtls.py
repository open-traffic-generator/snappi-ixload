import snappi

api = snappi.api(location="10.154.163.25:8080", ext="ixload", verify=False)
config = api.config()

port_1 = config.ports.port(name="p1", location="amit.buh.is.keysight.com/1/2")[-1]
port_2 = config.ports.port(name="p2", location="amit.buh.is.keysight.com/2/2")[-1]

(d1, d2,) = config.devices.device(name="d1").device(name="d2")
(e1,) = d1.ethernets.ethernet(name="d1.e1")
e1.connection.port_name = "p1"
e1.mac = "70:9C:91:69:00:00"
e1.step = "00:00:00:00:00:01" 
e1.count = 1

(e2,) = d2.ethernets.ethernet(name="d2.e2")
e2.connection.port_name = "p2"
e2.mac = "7C:5D:68:26:00:00"

(msdtls1,) = d1.mmacdtls.macdtls(name="Microdtls")
msdtls1.tunnel_dest_mac_start = "AA:BB:CC:DD:EE:FF"
msdtls1.tunnel_dest_mac_incr = "00:00:00:00:00:01"
msdtls1.in_key = "0xBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"

(m_val1, )= msdtls1.vlan()
m_val1.vlan_id = 1
m_val1.incr = 1
m_val1.count = 1
m_val1.tag = "0x8100"
m_val1.priority = 0

(m_ip1, )= msdtls1.ip()
m_ip1.start = "10.0.0.10"

(m_nm1, )= msdtls1.network_mesh()
m_nm1.mapping_type = "full mesh"
