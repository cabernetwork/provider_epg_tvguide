# pylama:ignore=E203,E221
"""
MIT License

Copyright (C) 2023 ROCKY4546
https://github.com/rocky4546

This file is part of Cabernet

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
"""

from lib.tvheadend.epg_category import groups
from lib.tvheadend.epg_category import tvh_genres

tvguide_base = 'gfpMXf5BjIU6ybXPXfiQtwS3Xx78tbhFyZrM'
tvguide_prog_details = 'jRkLjR33XxoQzftKkN37tfrEts5Qzft8zb7otqUGXZU8XZdPtxrMkb7EXIUT1qURtb2='
tvguide_ch_list = 'jRkLjR33XxoQzftKkN37tfrEts5Qzft8zb7otqUKtsiNgbl7XfiQzZ7ots2Q0RMQXNUCXZl7XIURtb2='
tvguide_sched = 'jRkLjR33XxoQzftKkN37tfrEts5Qzft8zb7otqUT1qURtb2VXRp3X8nU0RMZtfrIksp/yNJU0RMZkN33yZS7ydlQzsi6th7oXKCT1n=='
tvguide_image = 'gfpMXf5BjIURzRXFzft8zb7otqS6yNMQkqU/ybXQkNdMkbLQtG=='
tvguide_zones = 'bREYgbnYmYWS54WG5cWL545JjwWYyZdPtq2B2widkslMtsiF2wMerr5Y1qGe0Ii/tw2B2coL5cWG5c2G545E2wiFkbC726+e2ol7y8pIkbGejqarhIiUjwaT2Z7o26+em49K5KWG56eSmqGe2ZS3ybhYmYWY4bUCy8p3gbJejqarhIiUjwaT2Z7o26+em49K5KWG5c2J5qGe2ZS3ybhYmYWYhxd6gbt/kIWP2dr428ME2fEYgbnYmYWS54WG5cWNl49MjwWYyZdPtq2B2wiayxdKgNdF2wMerr5Y1qGe0Ii/tw2B2coL5K5G5ckSm42E2wiFkbC726+e2o33zNd/gbdF2wMerr5Y1rM='


tv_genres = {
    "Action & Adventure": [ tvh_genres['THRILLER'] ],
    "Advice":     [ tvh_genres['TALK_SHOW'] ],
    "Animals":    [ tvh_genres['NATURE'] ],
    "Animated":   [ tvh_genres['CARTOON'] ],
    "Cartoon":    [ tvh_genres['CARTOON'] ],
    "Comedy":     [ tvh_genres['COMEDY'] ],
    "Countdown":  [ tvh_genres['TALK_SHOW'] ],
    "Courtroom":  [ tvh_genres['SOCIAL'] ],
    "Crime":      [ tvh_genres['SOCIAL'] ],
    "Current Affairs": [ tvh_genres['SOCIAL'] ],
    "Documentary": [ tvh_genres['DOCUMENTARY'] ],
    "Drama":      [ tvh_genres['MOVIE'] ],
    "Educational": [ tvh_genres['EDUCATIONAL'] ],
    "Entertainment":  [ tvh_genres['GAME'] ],
    "Family":     [ tvh_genres['KIDS_6_14'] ],
    "Fantasy":    [ tvh_genres['SF'] ],
    "Game Show":  [ tvh_genres['GAME'] ],
    "Home & Garden": [ tvh_genres['GARDENING'] ],
    "Horror":     [ tvh_genres['SF'] ],
    "Infomercial":  [ tvh_genres['SHOPPING'] ],
    "Kids":       [ tvh_genres['KIDS'] ],
    "Magazine":   [ tvh_genres['NEWS_MAGAZINE'] ],
    "Music":      [ tvh_genres['MUSIC'] ],
    "Mystery & Suspense":  [ tvh_genres['THRILLER'] ],
    "Newscast":  [ tvh_genres['NEWS'] ],
    "Newsmagazine":  [ tvh_genres['NEWS_MAGAZINE'] ],
    "Politics":  [ tvh_genres['NEWS'] ],
    "Pro Wrestling":  [ tvh_genres['ATHLETICS'] ],
    "Public Affairs":  [ tvh_genres['BROADCASTING'] ],
    "Religion":  [ tvh_genres['RELIGION'] ],
    "Soccer":  [ tvh_genres['FOOTBALL'] ],
    "Business":   [ tvh_genres['NEWS'] ],
    "Other":      None,
    "Pro Sports": [ tvh_genres['SPORT'] ],
    "Reality":    [ tvh_genres['GAME'] ],
    "Science":    [ tvh_genres['SCIENCE'] ],
    "Science Fiction": [ tvh_genres['SF'] ],
    "Sports":     [ tvh_genres['SPORT'] ],
    "Suspense":   [ tvh_genres['THRILLER'] ],
    "Talk & Interview": [ tvh_genres['TALK_SHOW'] ],
    "Travel":     [ tvh_genres['TRAVEL'] ],
    "Tech & Gaming": [ tvh_genres['TECHNOLOGY'] ],
    "Variety Shows": [ tvh_genres['VARIETY'] ]
 }