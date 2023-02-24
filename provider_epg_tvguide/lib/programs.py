# pylama:ignore=E722
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

import datetime
import json
import re
import string
import time
import urllib.request

import lib.common.exceptions as exceptions
import lib.common.utils as utils
from lib.common.decorators import handle_url_except
from lib.common.decorators import handle_json_except
from lib.db.db_epg_programs import DBEpgPrograms
from lib.plugins.plugin_programs import PluginPrograms
from .translations import tv_genres


class Programs(PluginPrograms):

    def __init__(self, _instance_obj):
        super().__init__(_instance_obj)
        self.db_programs = DBEpgPrograms(self.config_obj.data)


    def get_program_info(self, _prog_id):
        """
        returns the prog info.  if not in database, then will 
        get it from provider and update database.
        """
        program = self.db_programs.get_program(self.plugin_obj.name, _prog_id)
        if len(program) != 0:
            return program

        uri = self.plugin_obj.unc_tvguide_base + self.plugin_obj.unc_tvguide_prog_details.format(_prog_id)
        prog_details = self.get_uri_data(uri)

        prog_details = prog_details['data']['item']
        if prog_details['title'] is None:
            prog_details['title'] = prog_details['name']

        self.logger.debug('{}:{} Adding Program {} {} to db' \
            .format(self.plugin_obj.name, self.instance_key, _prog_id, prog_details['title']))

        if len(prog_details['images']) != 0:
            image_bucket = prog_details['images'][0]['bucketPath']
            image_url = self.plugin_obj.unc_tvguide_image + image_bucket
        else:
            image_url = None

        if len(prog_details['genres']) == 0:
            genres = None
        else:
            genres = prog_details['genres'][0]['name']
            if genres == 'Other':
                if len(prog_details['genres']) == 1:
                    genres = string.capwords(prog_details['genres'][0]['genres'][0])
                else:
                    genres = prog_details['genres'][len(prog_details['genres'])-1]['name']
            if genres in tv_genres:
                genres = tv_genres[genres]
            else:
                self.logger.info('Missing TVGuide genre translation for: {}' \
                        .format(genres))
                genres = [genres]

        if prog_details['episodeNumber'] == 0:
            episode = None
        else:
            episode = prog_details['episodeNumber']

        if prog_details['episodeAirDate'] is None:
            pass
        elif prog_details['episodeAirDate'].startswith('/Date'):
            m = re.search('Date\((\d*)\)', prog_details['episodeAirDate'])
            if m is None:
                prog_details['episodeAirDate'] = None
            else:
                prog_details['episodeAirDate'] = m.group(1)
        else:
            self.logger.warning('{}:{} Unknown format for episodeAirDate. Program:{}  Date:{}' \
                .format(self.plugin_obj.name, self.instance_key, _prog_id, prog_details['episodeAirDate']))

        if prog_details['releaseYear']:
            year = str(prog_details['releaseYear'])
        else:
            year = prog_details['releaseYear']

        program = { 
            'title':      prog_details['title'], 
            'desc':       prog_details['description'],
            'short_desc': prog_details['description'],
            'rating':     prog_details['tvRating'],
            'year':       prog_details['releaseYear'],
            'date':       prog_details['episodeAirDate'],
            'type':       prog_details['type'],
            'episode':    episode,
            'season':     prog_details['seasonNumber'],
            'subtitle':   prog_details['episodeTitle'],
            'genres':     genres,
            'image':      image_url}

        self.db_programs.save_program(self.plugin_obj.name, _prog_id, program)
        return self.db_programs.get_program(self.plugin_obj.name, _prog_id)