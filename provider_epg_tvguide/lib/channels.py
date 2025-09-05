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

import re
import time

from lib.plugins.plugin_channels import PluginChannels
from lib.common.decorators import handle_json_except
from lib.common.decorators import handle_url_except
import lib.common.utils as utils


class Channels(PluginChannels):

    def __init__(self, _instance_obj):
        super().__init__(_instance_obj)
        self.down_timer = 0  # stop running queries to website when errors start occurring
        self.search_url = re.compile(b'iframe src=\"(.*?)\" width')
        self.search_m3u8 = re.compile(b'source:\'(.*?)\'')
        self.search_ch = re.compile(r'div class="grid-item">'
                                    + r'<a href=\"(\D+(\d+).php.*?)\" target.*?<strong>(.*?)</strong>')
        self.ch_db_list = None

    def get_channels(self):
        self.logger.warning('####### CALLING GET_CHANNELS #######')
        return

    @handle_url_except(timeout=10.0)
    @handle_json_except
    def get_channel_ref(self, _channel_id):
        self.logger.warning('####### CALLING GET_CHANNEL_REF #######')
        return

    @handle_url_except(timeout=10.0)
    @handle_json_except
    def get_channel_uri(self, _channel_id):
        self.logger.warning('####### CALLING GET_CHANNEL_URI #######')
        return

    def get_channel_list(self, _zone, _ch_ids=None):
        """
        returns the list of channels associated with the zone
        All if _ch_ids is None
        """
        ch_list = []

        tvg_json = self.get_zone_data(_zone)
        if tvg_json is None:
            return
        for ch in tvg_json['data']['items']:

            if _ch_ids is not None and ch['sourceId'] not in _ch_ids:
                continue
            if [u for u in ch_list if u['id'] == ch['sourceId']]:
                # found duplicate entries from provider, ignoring
                continue

            uid = ch['sourceId']
            name = ch['fullName']
            if name.lower().startswith('the '):
                name = name[4:]
            thumb = self.plugin_obj.unc_tvguide_image + ch['logo']
            enabled = True
            channel = {
                'id': uid,
                'enabled': enabled,
                'callsign': ch['name'],
                'number': 0,
                'name': name,
                'HD': 0,
                'group_hdtv': None,
                'group_sdtv': None,
                'groups_other': None,
                'thumbnail': thumb,
                'thumbnail_size': None,
                'VOD': False,
                'plugin': 'TVGuide',
                'epg_id': [_zone, uid]
            }
            ch_list.append(channel)
            self.logger.trace('{} Added Channel {}:{}'.format(self.plugin_obj.name, uid, name))
        return ch_list

    def get_zone_data(self, _zone):
        self.plugin_obj.check_ua_timer()
        tvg_json = None
        while self.plugin_obj.user_agent:
            uri = self.plugin_obj.append_apikey(
                self.plugin_obj.unc_tvguide_base + \
                self.plugin_obj.unc_tvguide_ch_list.format(_zone))
            tvg_json = self.get_uri_json_data(uri, 2, _header=self.plugin_obj.header)
            time.sleep(self.config_obj.data[self.plugin_obj.namespace.lower()]['http_delay'])
            if tvg_json is None:
                self.logger.notice('{}:{} No channels returned for Zone: {}  UA Index: {}'
                    .format(self.plugin_obj.name, self.instance_key, _zone, self.plugin_obj.ua_index))
                self.plugin_obj.incr_ua()
            else:
                return tvg_json
        if not tvg_json:
            self.logger.debug('{}:{} Website is restricted.  Wait a long time before running again. Zone: {}  UA Index: {}'
                    .format(self.plugin_obj.name, self.instance_key, _zone, _uid, self.plugin_obj.ua_index))
        return

    def get_default_zones(self):
        zones = self.db.get_zones(self.plugin_obj.name, self.instance_key)
        if not len(zones):
            for zone in self.plugin_obj.zone_defaults:
                self.db.add_zone(self.plugin_obj.name, self.instance_key, zone['id'], zone['name'])
        return zones
