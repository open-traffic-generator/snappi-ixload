import json
import re
import time
from snappi_ixload.timer import Timer


class objective_config():
    """Timeline and objective class config
    """
    _CONSTRAINT_TYPES = { 
        "simulated_user": "SimulatedUserConstraint",
        "connection_per_sec": "ConnectionRateConstraint",
        "concurrent_connections": "ConcurrentConnectionsConstraint",
        "transactions_per_sec": "TransactionRateConstraint"}

    _OBJECTIVE_TYPES = { "simulated_user": "simulatedUsers",
                         "throughput_kbps": "throughputKbps",
                         "throughput_mbps": "throughputMbps",
                         "connection_per_sec": "connectionRate",
                         "concurrent_connections": "concurrentConnections",
                         "connection_attempts_per_sec": "connectionAttemptRate",
                         "transactions_per_sec": "transactionRate"}

    _SIMULATED_USERS_CONFIGS = { 
        "ramp_up_type": "rampUpType",
        "ramp_up_interval": "rampUpInterval",
        "ramp_up_value": "rampUpValue",
        "sustain_time": "sustainTime",
        "ramp_down_time": "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment",
        "iteration": "iterations",
        "time_to_first_iter":  "standbyTime",
        "iteration_time": "iterationTime",  # can be set to only max_user rampup type
        "ramp_down_value": "rampDownValue",
        # "ramp_up_time" : "rampUpTime" #read-only attribute
    }

    _CONCURRENT_CONNECTIONS_CONFIGS = { 
        "ramp_down_value": "rampDownValue",
        "sustain_time": "sustainTime",
        "ramp_down_time": "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment",
        "iteration": "iterations",
        "time_to_first_iter":  "standbyTime"
    }

    _COMMON_CONFIGS = { 
        "sustain_time": "sustainTime",
        "ramp_down_time": "rampDownTime",
        "enable_controlled_user_adjustment": "checkEdit_enableControlledUserAdjustment",
        "iteration": "iterations",
        "time_to_first_iter":  "standbyTime"
    }

    _USER_PAYLOAD = ["rampUpType", "rampUpInterval", "rampUpValue", "sustainTime",
                     "rampDownTime", "checkEdit_enableControlledUserAdjustment",
                     "iterations", "standbyTime", "rampDownValue"]

    _MAX_PAYLOAD = ["rampUpType", "rampUpValue", "rampDownTime", "checkEdit_enableControlledUserAdjustment",
                    "iterations", "standbyTime", "iterationTime", "rampDownValue"]

    _IMMEDIATE_PAYLOAD = ["rampUpType",  "sustainTime", "rampDownTime",
                          "checkEdit_enableControlledUserAdjustment",
                          "iterations", "standbyTime", "rampDownValue"]

    _RAMP_TYPE = {"users_intervals": 0, "max_pending_user": 1, "immediate": 2}

    _VALIDATE_RAMP_TYPE = {"users_intervals": _USER_PAYLOAD,
                           "max_pending_user": _MAX_PAYLOAD,
                           "immediate": _IMMEDIATE_PAYLOAD}

    def __init__(self, ixloadapi):
        self._api = ixloadapi

    def config(self):
        """
        """
        self._config = self._api._l47config
        with Timer(self._api, "Objective Configurations"):
            for device in self._config.devices:
                for http in device.https:
                    for http_client in http.clients:
                        self._configure_objective_config(http_client)

    def _create_timeline(self, timeline_name):
        url = "%s/ixload/test/activeTest/timelineList" % (self._api._ixload)
        timeline_payload = {"name": timeline_name}
        response = self._api._request('POST', url, timeline_payload)

    def _get_timeline(self, timeline_name):
        url = "%s/ixload/test/activeTest/timelineList" % (self._api._ixload)
        timelinelist = self._api._request('GET', url, {})
        for timeline in timelinelist:
            if timeline['name'] == timeline_name:
                index = timeline['objectID']
                return index
        return None
    
    def _get_objective_payload(self, index, objective_type, objective_value, timeline_index):
        obj_payload = {}
        if len(objective_type) > 2:
            obj_payload["secondaryEnableConstraint"] = "True"
            obj_payload["secondaryConstraintType"] = objective_config._CONSTRAINT_TYPES[objective_type[index+2]]
            obj_payload["secondaryConstraintValue"] = objective_value[index+2]
        if len(objective_type) > 1:
            obj_payload["enableConstraint"] = "True"
            obj_payload["constraintType"] = objective_config._CONSTRAINT_TYPES[objective_type[index+1]]
            obj_payload["constraintValue"] = objective_value[index+1]
        obj_payload["timelineId"] = timeline_index
        obj_payload["userObjectiveType"] = objective_config._OBJECTIVE_TYPES[objective_type[index]]
        obj_payload["userObjectiveValue"] = objective_value[index]
        return obj_payload

    def _extract_ramptype_payload(self, payload, objective_type):
        """To extract ramp up type timeline attritubes
        """
        temp_payload = {}
        if 'rampUpType' in payload.keys():
            validate_list = objective_config._VALIDATE_RAMP_TYPE[payload['rampUpType']]
            temp_payload['rampUpType'] = objective_config._RAMP_TYPE[payload['rampUpType']]
            payload.pop('rampUpType')
        else :
            validate_list = objective_config._VALIDATE_RAMP_TYPE['users_intervals']
        for attr in payload.keys():
            if attr in validate_list:
                temp_payload.update({attr:payload[attr]})
        return temp_payload
    
    def _configure_objective_config(self, http_client):
        """Add any scenarios to the api server that do not already exist
        """
        for trafficprofile in self._config.trafficprofile:
            payload = {}
            index = 0
            objective_type = trafficprofile.objective_type[index]
            if "simulated_user" == objective_type:
                payload = self._api._set_payload(trafficprofile.objectives[index].simulated_user, objective_config._SIMULATED_USERS_CONFIGS)
                payload = self._extract_ramptype_payload(payload, objective_type)
            if "throughput_kbps" == objective_type:
                payload = self._api._set_payload(trafficprofile.objectives[index].throughput_kbps, objective_config._COMMON_CONFIGS)
            if "throughput_mbps" == objective_type:
                payload = self._api._set_payload(trafficprofile.objectives[index].throughput_mbps, objective_config._COMMON_CONFIGS)
            if "connection_per_sec" == objective_type:
                payload = self._api._set_payload(trafficprofile.objectives[index].connection_per_sec, objective_config._COMMON_CONFIGS)
            if "concurrent_connections" == objective_type:
                payload = self._api._set_payload(trafficprofile.objectives[index].concurrent_connections, objective_config._CONCURRENT_CONNECTIONS_CONFIGS)
            if "connection_attempts_per_sec" == objective_type:
                payload = self._api._set_payload(trafficprofile.objectives[index].connection_attempts_per_sec,
                                                    objective_config._COMMON_CONFIGS)
            if "transactions_per_sec" == objective_type:
                payload = self._api._set_payload(trafficprofile.objectives[index].transactions_per_sec, 
                                                        objective_config._COMMON_CONFIGS)
            timeline_index = self._get_timeline(trafficprofile.timeline[index])
            if timeline_index == None:
                self._create_timeline(trafficprofile.timeline[index])
                timeline_index = self._get_timeline(trafficprofile.timeline[index])
            url = "%s/ixload/test/activeTest/timelineList/%s" % (self._api._ixload, timeline_index)
            response = self._api._request('PATCH', url, payload)
            obj_payload = self._get_objective_payload(index, trafficprofile.objective_type,
                                                      trafficprofile.objective_value, timeline_index)
            if http_client.name == trafficprofile.app[0]:
                url = self._api._config_url.get(http_client.name)
                response = self._api._request('PATCH', url, obj_payload)
        return