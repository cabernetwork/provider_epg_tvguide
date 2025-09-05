"""
MIT License

Copyright (C) 2023 ROCKY4546
https://github.com/rocky4546

This file is part of Cabernet

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
"""


from lib.plugins.plugin_handler import PluginHandler
from lib.db.db_channels import DBChannels
import lib.config.config_callbacks

def timeout_limit(_config_obj, _section, _key):

    try:
        if float(_config_obj.data[_section][_key]) < 0.5:
            _config_obj.data[_section][_key] = 1.1
            _config_obj.config_handler.set(_section, _key, "1.1")
            return 'ValueError: Value set too low, ignored'
        else:
            return
    except ValueError:
        _config_obj.data[_section][_key] = 1.1
        _config_obj.config_handler.set(_section, _key, "1.1")
        return 'ValueError: Illegal Value, ignored'
    

