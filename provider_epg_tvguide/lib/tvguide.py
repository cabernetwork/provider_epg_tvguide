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

        for inst in _plugin.instances:
            self.instances[inst] = TVGuideInstance(self, inst)
