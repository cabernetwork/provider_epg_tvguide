# pylama:ignore=E203,E221
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

from lib.tvheadend.epg_category import tvh_genres

tvguide_base = 'gfpMXf5BjIUYkblOtbSoj8pNtRr/txhFkNUP'
tvguide_prog_details = 'jRkLjR33XxoQzftKkN37tfrEts5Qzft8zb7otqUGXZU8XZdPtxrMkb7EXIUT1qURtb2='
tvguide_ch_list = 'jRkLjR33XxoQzftKkN37tfrEts5Qzft8zb7otqUKtsiNgbl7XfiQzZ7ots2Q0RMQXNUCXZl7XIURtb2='
tvguide_sched = ''.join(['jRkLjR33XxoQzftKkN37tfrEts5Qzft8zb7otqUT1qURtb2VXRp3X8',
                         'nU0RMZtfrIksp/yNJU0RMZkN33yZS7ydlQzsi6th7oXKCT1n=='])
tvguide_image = 'gfpMXf5BjIURzRXFzft8zb7otqS6yNMQkqU/ybXQkNdMkbLQtG=='
tvguide_zones = ''.join([
    'bREYgbnYmYWS54WG5cWL545JjwWYyZdPtq2B2widkslMtsiF2wMerr5Y1qGe0Ii/tw2B2coL5cWG5c2G545E2wiFkbC726',
    '+e2ol7y8pIkbGejqarhIiUjwaT2Z7o26+em49K5KWG56eSmqGe2ZS3ybhYmYWY4bUCy8p3gbJejqarhIiUjwaT2Z7o26+e',
    'm49K5KWG5c2J5qGe2ZS3ybhYmYWYhxd6gbt/kIWP2dr428ME2fEYgbnYmYWS54WG5cWNl49MjwWYyZdPtq2B2wiayxdKgN',
    'dF2wMerr5Y1qGe0Ii/tw2B2coL5K5G5ckSm42E2wiFkbC726+e2o33zNd/gbdF2wMerr5Y1rM='])

tv_genres = {
    "Action & Adventure": [tvh_genres['THRILLER']],
    "Advice": [tvh_genres['TALK_SHOW']],
    "Animals": [tvh_genres['NATURE']],
    "Animated": [tvh_genres['CARTOON']],
    "Animated Comedy": [tvh_genres['CARTOON']],
    "Art": [tvh_genres['CULTURE']],
    "Auto Info": [tvh_genres['SPORT_MOTOR']],
    "Baseball": [tvh_genres['SPORT_TEAM']],
    "Basketball": [tvh_genres['SPORT_TEAM']],
    "Card Game": [tvh_genres['GAME']],
    "Cartoon": [tvh_genres['CARTOON']],
    "Comedy": [tvh_genres['COMEDY']],
    "Concert": [tvh_genres['CULTURE']],
    "Construction": [tvh_genres['HANDICRAFT']],
    "Countdown": [tvh_genres['TALK_SHOW']],
    "Courtroom": [tvh_genres['SOCIAL']],
    "Crime": [tvh_genres['SOCIAL']],
    "Current Affairs": [tvh_genres['SOCIAL']],
    "Decorating": [tvh_genres['HANDICRAFT']],
    "Documentary": [tvh_genres['DOCUMENTARY']],
    "Drama": [tvh_genres['MOVIE']],
    "Easy Listening": [tvh_genres['MUSIC']],
    "Educational": [tvh_genres['EDUCATIONAL']],
    "Entertainment": [tvh_genres['GAME']],
    "Espionage": [tvh_genres['THRILLER']],
    "Events & Specials": [tvh_genres['SPORT_SPECIAL']],
    "Family": [tvh_genres['KIDS_6_14']],
    "Fantasy": [tvh_genres['SF']],
    "Fishing": [tvh_genres['SPORT_WATER']],
    "Food & Cooking": [tvh_genres['COOKING']],
    "Game Show": [tvh_genres['GAME']],
    "Government": [tvh_genres['NEWS']],
    "Health & Lifestyle": [tvh_genres['FITNESS']],
    "History": [tvh_genres['HISTORICAL']],
    "Home & Garden": [tvh_genres['GARDENING']],
    "Horror": [tvh_genres['SF']],
    "Infomercial": [tvh_genres['SHOPPING']],
    "Kids": [tvh_genres['KIDS']],
    "Magazine": [tvh_genres['NEWS_MAGAZINE']],
    "Music": [tvh_genres['MUSIC']],
    "Mystery": [tvh_genres['THRILLER']],
    "Mystery & Suspense": [tvh_genres['THRILLER']],
    "Newscast": [tvh_genres['NEWS']],
    "Newsmagazine": [tvh_genres['NEWS_MAGAZINE']],
    "Politics": [tvh_genres['NEWS']],
    "Performance": [tvh_genres['PERFORMING']],
    "Pro Wrestling": [tvh_genres['ATHLETICS']],
    "Public Affairs": [tvh_genres['BROADCASTING']],
    "Religion": [tvh_genres['RELIGION']],
    "Soccer": [tvh_genres['FOOTBALL']],
    "Business": [tvh_genres['NEWS']],
    "Other": None,
    "Pro Sports": [tvh_genres['SPORT']],
    "Reality": [tvh_genres['GAME']],
    "Science": [tvh_genres['SCIENCE']],
    "Science Fiction": [tvh_genres['SF']],
    "Sports": [tvh_genres['SPORT']],
    "Suspense": [tvh_genres['THRILLER']],
    "Talk & Interview": [tvh_genres['TALK_SHOW']],
    "Travel": [tvh_genres['TRAVEL']],
    "Tech & Gaming": [tvh_genres['TECHNOLOGY']],
    "Variety Shows": [tvh_genres['VARIETY']],
    "Western": [tvh_genres['ADVENTURE']]
}
