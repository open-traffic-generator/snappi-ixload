import json
import re
import time
from snappi_ixload.timer import Timer

class objective_config():
    """
    """
   
    _SIMULATED_USERS_CONFIGS = { 
        #"ramp_up_type" : "rampUpType",
        "ramp_up_value" : "rampUpValue",
        "sustain_time" : "sustainTime",
        "ramp_down_time" : "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment"
    }  
    _CONCURRENT_PER_SECOND_CONFIGS = { 
        "sustain_time" : "sustainTime",
        "ramp_down_time" : "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment"
    }  
    _CONCURRENT_CONNECTIONS_CONFIGS = { 
        "ramp_down_value" : "rampDownValue",
        "sustain_time" : "sustainTime",
        "ramp_down_time" : "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment"
    }        
    _THROUGHPUT_CONFIGS = { 
        "sustain_time" : "sustainTime",
        "ramp_down_time" : "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment"
    }
    _TRANSACTIONS_CONFIG = { 
        "sustain_time" : "sustainTime",
        "ramp_down_time" : "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment"
    }
    _CONNECTION_ATTEMPT_CONFIGS = { 
        "sustain_time" : "sustainTime",
        "ramp_down_time" : "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment"
    }  
    _SEGMENT_CONFIGS = {
        "noise_amplitude_scale" : "noiseAmplitudeScale",
        "name" : "name",
        "start" : "startObjectiveScale",
        #"duration": "duration",
        #"rate":   "objectiveScaleDelta",
        "target": "endObjectiveScale"
    }

    _OBJECTIVE_TYPES = { "simulated_user" : "simulatedUsers",
                         "throughput_kbps" : "throughputKbps",
                         "throughput_mbps": "throughputMbps",
                         "connection_per_sec": "connectionRate",
                         "concurrent_connections": "concurrentConnections",
                         "connection_attempts_per_sec": "connectionAttemptRate",
                         "transactions_per_sec": "transactionRate"}
    def __init__(self, ixloadapi):
        self._api = ixloadapi
    
    def config(self):
        """
        """
        self._config = self._api._l47config
        #self._devices_config = self._api._l47config.devices
        with Timer(self._api, "Objective Configurations"):
            for device in self._config.devices:
                self._configure_objective_config()
            #self._configure_segment()
    
    def _configure_segment(self):
        """
        create segment to the timeline  that do not already exist
        """
        for trafficprofile in self._config.trafficprofile:
            url = "%s/ixload/test/activeTest/timelineList" %(self._api._ixload)
            timeline_list= self._api._request('GET', url)
            for timeline in timeline_list:
                for segment in trafficprofile.segment:
                    segment_url = url + "/%s/advancedIteration/segmentList" %(timeline['objectID'])
                    payload = self._api._set_payload(segment, objective_config._SEGMENT_CONFIGS)
                    response = self._api._request('POST', url, payload)
    
    def _create_timeline(self, timeline_name):
        url = "%s/ixload/test/activeTest/timelineList" % (self._api._ixload)
        timeline_payload = {"name" : timeline_name}
        response = self._api._request('POST', url, timeline_payload)
              
                                     
    def _get_timeline(self, timeline_name):
        url = "%s/ixload/test/activeTest/timelineList" % (self._api._ixload)
        timelinelist = self._api._request('GET', url, {})
        for timeline in timelinelist:
            if timeline['name'] == timeline_name:
                index = timeline['objectID']
                return index
        return None
            
    def _configure_objective_config(self):
        """Add any scenarios to the api server that do not already exist
        """
        for device in self._config.devices:
            for http in device.https:
                for trafficprofile in self._config.trafficprofile:
                    for objective_type in trafficprofile.objective_type:
                        index = trafficprofile.objective_type.index(objective_type)
                        if "simulated_user" == objective_type:
                            payload = self._api._set_payload(trafficprofile.objectives[index].simulated_user, objective_config._SIMULATED_USERS_CONFIGS)
                        if "throughput_kbps" == objective_type:
                            payload = self._api._set_payload(trafficprofile.objectives[index].throughput_kbps, objective_config._THROUGHPUT_CONFIGS)
                        if "throughput_mbps" == objective_type:
                            payload = self._api._set_payload(trafficprofile.objectives[index].throughput_mbps, objective_config._THROUGHPUT_CONFIGS)
                        if "connection_per_sec" == objective_type:
                            payload = self._api._set_payload(trafficprofile.objectives[index].connection_per_sec, objective_config._CONCURRENT_PER_SECOND_CONFIGS)
                        if "concurrent_connections" == objective_type:
                            payload = self._api._set_payload(trafficprofile.objectives[index].concurrent_connections, objective_config._CONCURRENT_CONNECTIONS_CONFIGS)
                        if "connection_attempts_per_sec" == objective_type:
                            payload = self._api._set_payload(trafficprofile.objectives[index].connection_attempts_per_sec,
                                                        objective_config._CONNECTION_ATTEMPT_CONFIGS)
                        if "transactions_per_sec" == objective_type:
                            payload = self._api._set_payload(trafficprofile.objectives[index].transactions_per_sec, 
                                                        objective_config._TRANSACTIONS_CONFIG)
                        timeline_index = self._get_timeline(trafficprofile.timeline[index])
                        if timeline_index == None:
                            self._create_timeline(trafficprofile.timeline[index])
                            timeline_index = self._get_timeline(trafficprofile.timeline[index])
                        url = "%s/ixload/test/activeTest/timelineList/%s" % (self._api._ixload, timeline_index)
                        response = self._api._request('PATCH', url, payload)
                        obj_payload = {}
                        obj_payload["timelineId"]=timeline_index
                        obj_payload["userObjectiveType"] = objective_config._OBJECTIVE_TYPES[objective_type]
                        obj_payload["userObjectiveValue"]  = trafficprofile.objective_value[index]
                        comunity_url = "%s/ixload/test/activeTest/communityList" % (self._api._ixload)
                        comunity_list = self._api._request('GET', comunity_url, {})
                        for comunity in comunity_list:
                            if comunity['role'] == 'Client':
                                activity_url = "%s/%s/activityList" % (comunity_url, comunity['objectID'])
                                activity_list = self._api._request('GET', activity_url, {})
                                for activity in activity_list:
                                    txt = http.name[: 4] + "Client" + http.name[4:]
                                    if txt == activity['name']:
                                        url = "%s/%s" %(activity_url, activity['objectID'])
                                        response = self._api._request('PATCH', url, obj_payload)