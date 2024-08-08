import json
import re
from brisk_ixload.timer import Timer


class protocols(object):
    """Transforms OpenAPI objects into IxLoad objects
    - network to /network
    Args
    ----
    - ixloadapi (Api): instance of the Api class
    """
    
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """Transform config.network into IxLoad.network
        1) create a network for every config.scenarios.networks that is not present in IxLoad
        2) set config.networks[].name to /network -name using rest call
        """
        self._scenarios_config = self._api.brisk_config.scenarios
        with Timer(self._api, "Protocol Configuration"):
            self._create_protocol(self._scenarios_config)
    
    def _create_protocol(self, scenarios):
        """Add any network to the api server that do not already exist
        """
        for scenario in scenarios:
            for network in scenario.networks:
                if network.protocols:
                    for protocol in network.protocols:
                        if protocol.httpclient:
                            url1, url2 = self._api._get_url(scenario.url , protocol.url)
                            payload = {"protocolAndType":"HTTP Client"}
                            response = self._api._request('POST', url1, payload)
                            protocol.url = url1 + response + url2
                            for agent in protocol.httpclient:
                                self._configure_protocol(agent, protocol.url)
                                for cmd in agent.commands:        
                                    self._configure_command(cmd, agent.url)
                        if protocol.httpserver:
                            url1, url2 = self._api._get_url(scenario.url , protocol.url)
                            payload = {"protocolAndType":"HTTP Server"}
                            response = self._api._request('POST', url1, payload)
                            protocol.url = url1 + response + url2
                            for agent in protocol.httpserver:
                                #import pdb; pdb.set_trace()
                                self._configure_protocol(agent, protocol.url)
                                #for cmd in agent.commands:        
                                    #self._configure_command(cmd, agent.url)

    def _configure_protocol(self, agent, protocol_url):
        """Add any network to the api server that do not already exist
        """
        agent.url = protocol_url + agent.url
        payload = self._api._set_payload(agent)
        if payload:
            #import pdb; pdb.set_trace()
            self._api._request('PATCH', agent.url, payload)
        return

    def _configure_command(self, cmd, agent_url):
        """Add any network to the api server that do not already exist
        """
        cmd.url = agent_url + cmd.url
        payload = self._api._set_payload(cmd)
        #import pdb; pdb.set_trace()
        if payload:
            #import pdb; pdb.set_trace()
            self._api._request('POST', cmd.url, payload)
        return

