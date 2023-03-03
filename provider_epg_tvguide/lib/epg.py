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

from lib.plugins.plugin_epg import PluginEPG
from lib.db.db_temp import DBTemp


class EPG(PluginEPG):

    def __init__(self, _instance_obj):
        super().__init__(_instance_obj)
        self.db_temp = DBTemp(self.config_obj.data)

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

            json_data = self.get_uri_data(uri)
            if json_data is None:
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
