# pylama:ignore=E722
"""
MIT License

Copyright (C) 2023 ROCKY4546

This file is part of the TVGuide plugin and is not associated with any other repository

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
"""

import datetime
import json
import time

from lib.plugins.plugin_epg import PluginEPG
from lib.db.db_temp import DBTemp
import lib.common.utils as utils


class EPG(PluginEPG):

    def __init__(self, _instance_obj):
        super().__init__(_instance_obj)
        self.db_temp = DBTemp(self.config_obj.data)
        self.down_timer = 0

    def get_channel_day(self, _zone, _uid, _day_seconds):
        """
        For a channel (uid) in a zone (like a zipcode), return
        a dict listed by day with all programs listed for that day within it.
        This interface is for the epg plugins
        _day_seconds is time in seconds at midnight
        """

        # default is setup to purge data every 6 hours for specific insance
        self.db_temp.cleanup_temp(self.plugin_obj.name, self.instance_key)
        tvg_ch = self.db_temp.get_record(self.plugin_obj.name, self.instance_key, str(_zone) + '_' + str(_uid))
        if tvg_ch:
            tvg_ch = json.loads(tvg_ch[0]['json'])
        else:
            # get the tvg channel data from provider

            current_time = datetime.datetime.now(datetime.timezone.utc)
            start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
            start_seconds = int(start_time.timestamp())
            min_dur = 20160

            uri = self.plugin_obj.unc_tvguide_base + \
                self.plugin_obj.unc_tvguide_sched \
                    .format(_zone, start_seconds, min_dur, _uid)
            time.sleep(0.5)
            if self.down_timer > 0:
                self.down_timer -= 1
                self.logger.notice('{}:{} Errors occuring on EPG queries, skipping for uid {}'
                                    .format(self.plugin_obj.name, self.instance_key, _uid))
                return
            else:
                header = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Host': 'backend.tvguide.com',
                    'Priority': 'u=0, i',
                    #'User-agent': utils.DEFAULT_USER_AGENT,
                    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',
                    #'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
                    'Referer': 'https://www.tvguide.com/',
                    'Origin': 'https://www.tvguide.com'}

                json_data = self.get_uri_data(uri, 2, _header=header)
                # TVG thinks DDOS if not slow pulls, so put time delays into method.
                if json_data is None:
                    self.down_timer = 200
                    return None
            if len(json_data['data']['items']) == 0:
                self.logger.notice('TVGuide Zone: {}  UID: {} has no programs'
                    .format(_zone, _uid))
                return None

            json_data = json_data['data']['items'][0]['programSchedules']
            end_time = start_time + datetime.timedelta(days=1)
            end_seconds = int(end_time.timestamp())
            prog_list = {}
            day_list = []
            for prog in json_data:
                if prog['startTime'] > end_seconds:
                    prog_list[start_seconds] = day_list
                    day_list = []
                    start_time = end_time
                    start_seconds = end_seconds
                    end_time = start_time + datetime.timedelta(days=1)
                    end_seconds = int(end_time.timestamp())
                day_list.append({
                    'id': prog['programId'],
                    'channelId': _uid,
                    'progId': prog['programId'],
                    'start': prog['startTime'],
                    'end': prog['endTime'],
                    'title': prog['title'],
                    'rating': prog['rating']
                })
            if day_list:
                prog_list[start_seconds] = day_list
                day_list = []

            self.db_temp.save_json(self.plugin_obj.name, self.instance_key, str(_zone) + '_' + str(_uid), prog_list)
            # json requirements are different than Python so need to convert to JSON format and back
            # so it will be the same as what is in the database
            tvg_ch = json.loads(json.dumps(prog_list))
        return tvg_ch.get(str(_day_seconds))
