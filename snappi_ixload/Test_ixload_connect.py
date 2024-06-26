import ixloadapi
import brisk
cObj = brisk.Api().config()
scObj = cObj.scenarios.scenario().scenario().scenario()
nwObj = scObj[-1].networks.network()
etObj = nwObj[-1].ethernet.ethernet()
ipv4Obj = nwObj[-1].ipv4.ipv4()

api = ixloadapi.Api("10.22.45.55", ixload_version = "8.50.0.465")
api.set_config(cObj)
print("*****")
print(cObj)
print("*****")
