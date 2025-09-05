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

import re
import string
import time

from lib.db.db_epg_programs import DBEpgPrograms
from lib.plugins.plugin_programs import PluginPrograms
from .translations import tv_genres
import lib.common.utils as utils


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

        prog_details = None
        self.plugin_obj.check_ua_timer()
        while self.plugin_obj.user_agent:
            uri = self.plugin_obj.append_apikey(
                self.plugin_obj.unc_tvguide_base + \
                    self.plugin_obj.unc_tvguide_prog_details.format(_prog_id))

            prog_details = self.get_uri_data(uri, 2, _header=self.plugin_obj.header)
            time.sleep(self.config_obj.data[self.plugin_obj.namespace.lower()]['http_delay'])
            if prog_details is None:
                self.logger.notice('{}:{} No program details returned for Prog_ID: {}  UA Index: {}'
                    .format(self.plugin_obj.name, self.instance_key, _prog_id, self.plugin_obj.ua_index))
                self.plugin_obj.incr_ua()
            else:
                break

        if not prog_details:
            return []
            # for programs that do not have detailed info, provide a default set
            #program = {
            #    'title': 'Not Available',
            #    'desc': 'Not Available',
            #    'short_desc': 'Not Available',
            #    'rating': None,
            #    'year': None,
            #    'date': None,
            #    'type': None,
            #    'episode': None,
            #    'season': None,
            #    'subtitle': None,
            #    'genres': None,
            #    'image': None}

            #self.db_programs.save_program(self.plugin_obj.name, _prog_id, program)
            #return self.db_programs.get_program(self.plugin_obj.name, _prog_id)

        prog_details = prog_details['data']['item']
        if prog_details['title'] is None:
            prog_details['title'] = prog_details['name']

        self.logger.debug('{}:{} Adding Program {} {} to db'
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
                    genres = prog_details['genres'][len(prog_details['genres']) - 1]['name']
            if genres in tv_genres:
                genres = tv_genres[genres]
            else:
                self.logger.info('Missing TVGuide genre translation for: {}'
                                 .format(genres))
                genres = [genres]

        if prog_details['episodeNumber'] == 0:
            episode = None
        else:
            episode = prog_details['episodeNumber']

        if prog_details['episodeAirDate'] is None:
            pass
        elif prog_details['episodeAirDate'].startswith('/Date'):
            m = re.search(r'Date\((\d*)\)', prog_details['episodeAirDate'])
            if m is None:
                prog_details['episodeAirDate'] = None
            else:
                prog_details['episodeAirDate'] = m.group(1)
        else:
            self.logger.warning('{}:{} Unknown format for episodeAirDate. Program:{}  Date:{}'
                                .format(self.plugin_obj.name, self.instance_key, _prog_id,
                                        prog_details['episodeAirDate']))

        program = {
            'title': prog_details['title'],
            'desc': prog_details['description'],
            'short_desc': prog_details['description'],
            'rating': prog_details['tvRating'],
            'year': prog_details['releaseYear'],
            'date': prog_details['episodeAirDate'],
            'type': prog_details['type'],
            'episode': episode,
            'season': prog_details['seasonNumber'],
            'subtitle': prog_details['episodeTitle'],
            'genres': genres,
            'image': image_url}

        self.db_programs.save_program(self.plugin_obj.name, _prog_id, program)
        return self.db_programs.get_program(self.plugin_obj.name, _prog_id)
