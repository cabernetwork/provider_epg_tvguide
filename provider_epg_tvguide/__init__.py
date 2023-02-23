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

import lib.plugins.plugin as plugin
from .lib.tvguide import TVGuide


# register the init plugin function
@plugin.register
def start(_plugin, _plugins):
    return TVGuide(_plugin)
