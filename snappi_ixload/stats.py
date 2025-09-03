import json
import re
import time
from datetime import datetime, timedelta

class stats_config():
    """
    """
    def __init__(self, ixloadapi):
        self._api = ixloadapi 
        self.test_state = False
        self.stats_dict = {}

    def _get_stats_list(self, req, name, metric_res):
        self.metric = metric_res
        if req.choice == "httpclient":
            self.stat_list = req.httpclient.stat_name
            all_stats_flag = req.httpclient.all_stats
            self.metric_http = self.metric.httpclient_metrics
        else:
            self.stat_list = req.httpserver.stat_name
            all_stats_flag = req.httpserver.all_stats
            self.metric_http = self.metric.httpserver_metrics
        if all_stats_flag:
            stats_source_list = self.get_statname_list(name)
        else:
            if not self.stat_list:
                raise Exception("Please provide stats name list")
            stats_source_list = [stat for stat in self.stat_list]
        return stats_source_list

    def poll_get_stats(self, name, metric_obj, metric_res):
        """
        get_stats - collects the stats information for the test
        """
        wait_time = datetime.now()+timedelta(0,300)
        poll_flag = True
        state = self._api.get_current_state()
        if (state.lower() == 'running' or state.lower() == 'starting run') :
            stats_client_source_url = "%s/ixload/stats/HTTPClient/values" % (self._api._ixload)
            stats_server_source_url = "%s/ixload/stats/HTTPServer/values" % (self._api._ixload)
            client_stats_source_list = self.get_statname_list("HTTPClient")
            server_stats_source_list = self.get_statname_list("HTTPServer")
            client_time_stamp_dict, server_time_stamp_dict = {} , {}
            client_time_stamp_dict = self.get_stat_timestamp_dict("HTTPClient", client_stats_source_list, client_time_stamp_dict)
            server_time_stamp_dict = self.get_stat_timestamp_dict("HTTPServer", server_stats_source_list, server_time_stamp_dict)
            stat_list, stat_list1 = [], []
            collected_timestamps, collected_timestamps1 = {}, {} 
            while self._api.get_current_state() == "Running" and poll_flag:
                values_dict = self._api._request('GET', stats_client_source_url, option=1)
                client_time_stamp_dict = self.get_running_stat(values_dict, client_stats_source_list, collected_timestamps, stat_list, client_time_stamp_dict, wait_time)
                values_dict1 = self._api._request('GET', stats_server_source_url, option=1)
                server_time_stamp_dict = self.get_running_stat(values_dict1, server_stats_source_list, collected_timestamps1, stat_list1, server_time_stamp_dict, wait_time)
                poll_flag = False
            self.stats_dict['httpclient'] = client_time_stamp_dict
            self.stats_dict['httpserver'] = server_time_stamp_dict
        return self.stat_metric(state, self.stats_dict, metric_obj, metric_res)        
    
    def get_stats(self, name, metric_obj, metric_res, test_state):
        """
        get_stats - collects the stats information for the test
        """
        wait_time = datetime.now()+timedelta(0,300)
        state = self._api.get_current_state()
        if (state.lower() == 'running' or state.lower() == 'starting run') and test_state == True:
            stats_client_source_url = "%s/ixload/stats/HTTPClient/values" % (self._api._ixload)
            stats_server_source_url = "%s/ixload/stats/HTTPServer/values" % (self._api._ixload)
            client_stats_source_list = self.get_statname_list("HTTPClient")
            server_stats_source_list = self.get_statname_list("HTTPServer")
            client_time_stamp_dict, server_time_stamp_dict = {} , {}
            client_time_stamp_dict = self.get_stat_timestamp_dict("HTTPClient", client_stats_source_list, client_time_stamp_dict)
            server_time_stamp_dict = self.get_stat_timestamp_dict("HTTPServer", server_stats_source_list, server_time_stamp_dict)
            stat_list, stat_list1 = [], []
            collected_timestamps, collected_timestamps1 = {}, {} 
            while self._api.get_current_state() == "Running" :
                values_dict = self._api._request('GET', stats_client_source_url, option=1)
                client_time_stamp_dict = self.get_running_stat(values_dict, client_stats_source_list, collected_timestamps, stat_list, client_time_stamp_dict, wait_time)
                values_dict1 = self._api._request('GET', stats_server_source_url, option=1)
                server_time_stamp_dict = self.get_running_stat(values_dict1, server_stats_source_list, collected_timestamps1, stat_list1, server_time_stamp_dict, wait_time)
            self.stats_dict['httpclient'] = client_time_stamp_dict
            self.stats_dict['httpserver'] = server_time_stamp_dict
        return self.stat_metric(state, self.stats_dict, metric_obj, metric_res)
    
    def stat_metric(self, state, stats_dict, metric_obj, metric_res):
        # metric_response        
        if len(stats_dict) > 0:
            if metric_obj.choice == 'httpclient':
                stat_value = stats_dict['httpclient']
                stats_source_list = self._get_stats_list(metric_obj, "HTTPClient", metric_res)
            else :
                stat_value = stats_dict['httpserver']     
                stats_source_list = self._get_stats_list(metric_obj, "HTTPServer", metric_res)   
            stats_value = {}  
            for key in stat_value.keys():
                for stats in stats_source_list:
                    if key == stats :
                        stats_value[key] = stat_value[key]
            for key, value in stats_value.items():
                index = list(stats_value.keys()).index(key)
                self.metric_http.metric(name=key)
                metric_stat = self.metric_http[index].stat_value
                metric_stat.stat_value(values=value['values'])
                stat_timestamp = metric_stat[0].timestamp
                for tmstamp, tmval in value['time_stamp'].items():
                    stat_timestamp.timestamp(timestamp_id=str(tmval[0]), value=str(tmval[1]))
            return self.metric
        else:
            raise Exception("Cannot Get Stats when ActiveTest is in %s State" % state)
        
    def get_statname_list(self, name):
        flag = True
        wait_time = datetime.now()+timedelta(0,300)
        stats_url = "%s/ixload/stats/%s/values" % (self._api._ixload, name)
        while flag:            
            stats_dict = self._api._request('GET', stats_url, option=1)
            if len(stats_dict) ==0 and  wait_time < datetime.now():
                raise Exception("Cannot Get Stats after 300 seconds.Check the test status")
            if stats_dict: flag = False 
        source_list_key  = [key for key  in stats_dict.keys()]
        source_list = [key for key in stats_dict[source_list_key[0]].keys()]
        return source_list
        
    def get_stat_timestamp_dict(self, name, source_list, time_stamp_dict):
        for stats in source_list:
            time_stamp_dict[stats] = {}
            time_stamp_dict[stats]['time_stamp'] = {}
            time_stamp_dict[stats]['values'] = []
        return  time_stamp_dict
            
    def get_running_stat(self, value_dict, stats_source_list,collected_timestamps, stat_list, time_stamp_dict, wait_time):
        if value_dict :
            for stats in stats_source_list:
                new_time_stamps = [int(timestamp) for timestamp in value_dict.keys() if timestamp  not  in collected_timestamps.get(stats, [])]
                new_time_stamps.sort()
                for timestamp in new_time_stamps:
                    time_stamp_str = str(timestamp)
                    if stats in value_dict[time_stamp_str].keys():
                        for caption, value in value_dict[time_stamp_str].items():
                            if caption == stats:
                                collected_timestamps.setdefault(stats, []).append(time_stamp_str)
                                key = 'timestamp'+str(collected_timestamps[stats].index(str(timestamp))+1)
                                time_stamp_dict[stats]['time_stamp'].update({key: (timestamp, str(value))})
                                time_stamp_dict[stats]['values'].append(str(value))
                    else:
                        raise Exception("Please enter the valid stats-%s is invalid" % stats) 
        if len(value_dict) ==0 and  wait_time < datetime.now():
            raise Exception("Cannot Get Stats after 300 seconds.Check the test status")
        return time_stamp_dict