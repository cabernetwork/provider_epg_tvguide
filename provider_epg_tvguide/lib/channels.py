"""
MIT License

Copyright (C) 2023 ROCKY4546
https://github.com/rocky4546

This file is part of the TVGuide plugin and is not associated with any other respository

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
"""

import base64
import datetime
import hashlib
import html
import json
import re
import socket
import sys
import threading
import time
import timeit
import urllib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from multiprocessing import Queue, Process

import lib.clients.channels.channels as channels
from lib.plugins.plugin_channels import PluginChannels
from lib.db.db_epg_programs import DBEpgPrograms
from lib.common.decorators import handle_json_except
from lib.common.decorators import handle_url_except
import lib.common.exceptions as exceptions
import lib.common.utils as utils


class Channels(PluginChannels):

    def __init__(self, _instance_obj):
        super().__init__(_instance_obj)
        self.search_url = re.compile(b'iframe src=\"(.*?)\" width')
        self.search_m3u8 = re.compile(b'source:\'(.*?)\'')
        self.search_ch = re.compile(r'div class="grid-item">'
            + '<a href=\"([^\d]+(\d+).php.*?)\" target.*?<strong>(.*?)<\/strong>')
        self.ch_db_list = None

    def get_channels(self):
        self.ch_db_list = self.db.get_channels(self.plugin_obj.name, self.instance_key)
        if self.ch_db_list:
            is_run_scans = False
        else:
            is_run_scans = True
        
        ch_list = self.get_channel_list()
        if len(ch_list) == 0:
            self.logger.warning('TVGuide channel list is empty from provider, not updating Cabernet')
            return
        self.logger.info("{}: Found {} stations on instance {}"
            .format(self.plugin_obj.name, len(ch_list), self.instance_key))
        ch_list = sorted(ch_list, key=lambda d: d['name'])
        ch_num = 1
        for ch in ch_list:
            ch['number'] = ch_num
            ch_num += 1
        return ch_list


    @handle_url_except(timeout=10.0)
    @handle_json_except
    def get_channel_ref(self, _channel_id):
        """
        gets the referer required to obtain the ts or stream files from server
        """
        text = self.get_uri_data(self.plugin_obj.unc_daddylive_base + \
            self.plugin_obj.unc_daddylive_stream.format(_channel_id))
        m = re.search(self.search_url, text)
        if not m:
            #unable to obtain the url, abort
            self.logger.info('{}: {} Unable to obtain url, aborting'
                .format(self.plugin_obj.name, _channel_id))
            return
        return m[1].decode('utf8')



    @handle_url_except(timeout=10.0)
    @handle_json_except
    def get_channel_uri(self, _channel_id):
        json_needs_updating = False
        ch_url = self.get_channel_ref(_channel_id)
        if not ch_url:
            return

        header = {
            'User-agent': utils.DEFAULT_USER_AGENT,
            'Referer': self.plugin_obj.unc_daddylive_base + self.plugin_obj.unc_daddylive_stream.format(_channel_id) }

        text = self.get_uri_data(ch_url, _header=header)
        m = re.search(self.search_m3u8, text)
        if not m:
            #unable to obtain the url, abort
            self.logger.notice('{}: {} Unable to obtain m3u8, aborting'
                .format(self.plugin_obj.name, _channel_id))
            return
        stream_url = m[1].decode('utf8')
        header = {
            'User-agent': utils.DEFAULT_USER_AGENT,
            'Referer': ch_url }
        videoUrlM3u = self.get_m3u8_data(stream_url, _header=header)
        if not videoUrlM3u:
            self.logger.notice('{}:{} Unable to obtain m3u file, aborting stream {}'
                .format(self.plugin_obj.name, self.instance_key, _channel_id))
            return            
        self.logger.debug('{}: Found {} Playlist(s)'
            .format(self.plugin_obj.name, str(len(videoUrlM3u.playlists))))

        ch_dict = self.db.get_channel(_channel_id, self.plugin_obj.name, self.instance_key)
        ch_json = ch_dict['json']
        
        bestStream = None
        bestResolution = -1
        if len(videoUrlM3u.playlists) > 0:
            for videoStream in videoUrlM3u.playlists:
                if videoStream.stream_info.resolution is not None:
                    if bestStream is None:
                        bestStream = videoStream
                        bestResolution = videoStream.stream_info.resolution[1]
                    elif ((videoStream.stream_info.resolution[0] > bestStream.stream_info.resolution[0]) and
                          (videoStream.stream_info.resolution[1] > bestStream.stream_info.resolution[1])):
                        bestResolution = videoStream.stream_info.resolution[1]
                        bestStream = videoStream
                    elif ((videoStream.stream_info.resolution[0] == bestStream.stream_info.resolution[0]) and
                          (videoStream.stream_info.resolution[1] == bestStream.stream_info.resolution[1]) and
                          (videoStream.stream_info.bandwidth > bestStream.stream_info.bandwidth)):
                        bestResolution = videoStream.stream_info.resolution[1]
                        bestStream = videoStream

            if bestStream is not None:
                if bestResolution >= 720 and ch_json['HD'] == 0:
                    ch_json['HD'] = 1
                    json_needs_updating = True
                elif bestResolution < 720 and ch_json['HD'] == 1:
                    ch_json['HD'] = 0
                    json_needs_updating = True
                
                self.logger.notice('{}: {} will use {}x{} resolution at {}bps' \
                    .format(self.plugin_obj.name, _channel_id, str(bestStream.stream_info.resolution[0]), \
                    str(bestStream.stream_info.resolution[1]), str(bestStream.stream_info.bandwidth)))
                m3u8_uri = bestStream.absolute_uri
            else:
                m3u8_uri = None
        else:
            self.logger.debug('{}: {} No variant streams found for this station.  Assuming single stream only.'
                .format(self.plugin_obj.name, _channel_id))
            m3u8_uri = stream_url

        if json_needs_updating:
            self.db.update_channel_json(ch_json, self.plugin_obj.name, self.instance_key)
        return m3u8_uri


    def get_channel_list(self, _zone, _ch_ids=None):
        """
        returns the list of channels associated with the zone
        All if _ch_ids is None
        """
        ch_list = []
        uri = self.plugin_obj.unc_tvguide_base + self.plugin_obj.unc_tvguide_ch_list.format(_zone)
        tvg_json = self.get_uri_json_data(uri)
        if tvg_json is None:
            self.logger.warning('{}:{} No channels returned for zone {} from tvguide'
                .format(self.plugin_obj.name, self.instance_key, _zone))
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
            hd = 0
            thumb_size = None
            epg_id = None
            
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
                'epg_id': [ _zone, uid ]
            }
            ch_list.append(channel)
            self.logger.debug('{} Added Channel {}:{}'.format(self.plugin_obj.name, uid, name))
        return ch_list
        

    def get_default_zones(self):
        zones = self.db.get_zones(self.plugin_obj.name, self.instance_key)
        if not len(zones):
            for zone in self.plugin_obj.zone_defaults:
                self.db.add_zone(self.plugin_obj.name, self.instance_key, zone['id'], zone['name'])
        return zones
