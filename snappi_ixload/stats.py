import json
import re
import time
from datetime import datetime, timedelta
#V1

class stats_config():
    """
    """
    def __init__(self, ixloadapi):
        self._api = ixloadapi 

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
            stats_url = "%s/ixload/stats/%s/availableStats" % (self._api._ixload, name)
            stats_dict = self._api._request('GET', stats_url, option=1)
            stats_source_list = [stat['statName'] for stat in stats_dict]
        else:
            if not self.stat_list:
                raise Exception("Please provide stats name list")
            stats_source_list = [stat for stat in self.stat_list]
        return stats_source_list

    def get_stats(self, name, metric_obj, metric_res):
        """
        get_stats - collects the stats information for the test
        """
        wait_time = datetime.now()+timedelta(0,300)
        state = self._api.get_current_state()
        if state.lower() == 'running' or state.lower() == 'starting run' :
            getting_stats = True
            stats_source_url = "%s/ixload/stats/%s/values" % (self._api._ixload, name)
            stats_source_list = self._get_stats_list(metric_obj, name, metric_res)
            collected_timestamps = {}
            time_stamp_dict = {}
            for stats in stats_source_list:
                time_stamp_dict[stats] = {}
                time_stamp_dict[stats]['time_stamp'] = {}
                time_stamp_dict[stats]['values'] = []
            values_dict = self._api._request('GET', stats_source_url, option=1)
            while getting_stats:
                if values_dict : # test start
                #if values_dict and self._api.get_current_state() == "Stopping Run" : # test end
                    for stats in stats_source_list:
                        new_time_stamps = [int(timestamp) for timestamp in values_dict.keys() if timestamp  not  in collected_timestamps.get(stats, [])]
                        new_time_stamps.sort()
                        stat_list = []
                        for timestamp in new_time_stamps:
                            time_stamp_str = str(timestamp)
                            if stats in values_dict[time_stamp_str].keys():
                                for caption, value in values_dict[  time_stamp_str].items():
                                    if caption == stats:
                                        stat_list.append(str(value))
                                        key = 'timestamp'+str(new_time_stamps.index(timestamp)+1)
                                        time_stamp_dict[stats]['time_stamp'].update({key: (timestamp, str(value))})
                                time_stamp_dict[stats]['values'] = stat_list
                            else:
                                raise Exception("Please enter the valid stats-%s is invalid" % stats)
                    stats_value = time_stamp_dict
                    getting_stats = False # get_stats for starting test
                    #getting_stats = self._api.get_current_state() == "Running" # get_stats for  ending test
                elif len(values_dict) ==0 and  wait_time < datetime.now():
                    raise Exception("Cannot Get Stats after 300 seconds.Check the test status")
                else:
                    values_dict = self._api._request('GET', stats_source_url, option=1)
        else:
            raise Exception("Cannot Get Stats when ActiveTest is in %s State" % state)
        # metric_response
        for key, value in stats_value.items():
            index = list(stats_value.keys()).index(key)
            self.metric_http.metric(name=key)
            metric_stat = self.metric_http[index].stat_value
            metric_stat.stat_value(values=value['values'])
            stat_timestamp = metric_stat[0].timestamp
            for tmstamp, tmval in value['time_stamp'].items():
                stat_timestamp.timestamp(timestamp_id=str(tmval[0]), value=str(tmval[1]))
        return self.metric
