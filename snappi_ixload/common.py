from snappi_ixload.logger import get_ixload_logger

class Common(object):
    def __init__(self):
        self.logger = get_ixload_logger(__name__)

    def get_ip_name(self, name):
        '''
            return the IP config from statefull flow endpoints.
        '''
        for app in self._api._apps:
            for flow in app.stateful_flows:
                if flow.client.protocol == name:
                    for endpoint in flow.client.endpoints:
                        return "e1.ipv4"
                elif flow.server.protocol == name:
                    for endpoint in flow.server.endpoints:
                        return "e2.ipv4"
    
    def get_protocol_ip(self, apps_obj):
        return_list = []
        for app in apps_obj.apps:
            for flow in app.stateful_flows:
                if flow.client.endpoints and flow.server.endpoints:
                    temp_dict, client, server = {}, {}, {}
                    for endpoint in flow.client.endpoints:
                        temp_dict[flow.client.protocol] = endpoint.ip_interface_name
                    for endpoint in flow.server.endpoints:
                        temp_dict[flow.server.protocol] = endpoint.dest.name               
                    #temp_dict['client'] = client
                    #temp_dict['server'] = server
                    #return_list.append(temp_dict)             
        return temp_dict

    
    def get_community_url(self, url):
        import re
        match = re.match(r'(.*\/communityList\/)(\d+)', url)
        if match:
            return (match.group(1)+match.group(2)+"/")