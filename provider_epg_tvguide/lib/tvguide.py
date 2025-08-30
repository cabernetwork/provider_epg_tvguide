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

import json
import time

from lib.plugins.plugin_obj import PluginObj

from .tvguide_instance import TVGuideInstance
from ..lib import translations


class TVGuide(PluginObj):

    def __init__(self, _plugin):
        super().__init__(_plugin)
        self.unc_tvguide_base = self.uncompress(translations.tvguide_base)
        self.unc_tvguide_prog_details = self.uncompress(translations.tvguide_prog_details)
        self.unc_tvguide_ch_list = self.uncompress(translations.tvguide_ch_list)
        self.unc_tvguide_sched = self.uncompress(translations.tvguide_sched)
        self.unc_tvguide_image = self.uncompress(translations.tvguide_image)
        self.zone_defaults = json.loads(self.uncompress(translations.tvguide_zones))
        self.api_key = ''

        self.user_agents = [
            'Mozilla/5.0 (Linux; Android 16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.7258.159 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone17,5; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 FireKeepers/1.7.0',
            'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            'Mozilla/5.0 (Android 16; Mobile; LG-M255; rv:142.0) Gecko/142.0 Firefox/142.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            None
        ]
        self.ua_index = 0
        self.ua_down_time = time.time()
        self.max_ua_down_time = 36000 # seconds (10 hours)

        for inst in _plugin.instances:
            self.instances[inst] = TVGuideInstance(self, inst)

    def incr_ua(self):
        if self.ua_index+1 < len(self.user_agents):
            self.ua_index += 1
            if self.ua_index+1 >= len(self.user_agents):
                self.ua_down_time = time.time()

    def check_ua_timer(self):
        if self.ua_index+1 >= len(self.user_agents):
            delta_down_time = time.time() - self.ua_down_time
            if delta_down_time > self.max_ua_down_time:
                self.logger.debug('{}: User Agent timeout exceeded.  Will try to reconnect to provider')
                self.ua_index = 0
                self.ua_down_time = time.time()
                return True
        return False

    def append_apikey(self, _uri):
        if not self.api_key:
            return _uri
        else:
            return _uri + '&apiKey=' + self.api_key

    @property
    def user_agent(self):
        return self.user_agents[self.ua_index]

    @property
    def header(self):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'backend.tvguide.com',
            'Priority': 'u=0, i',
            'User-agent': self.user_agent,
            'Referer': 'https://www.tvguide.com/',
            'Origin': 'https://www.tvguide.com'
        }
