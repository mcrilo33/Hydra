#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : utilities.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 17.10.2018
# Last Modified Date: 17.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import os
from time import strptime, mktime
from datetime import datetime

MUSIC_PATH = '/home/mcrilo33/Repos/MusicTest' # TO MOVE LATER
TORRENTS_PATH = os.path.join(MUSIC_PATH, '.torrents')
MUSIC_DATABASE_PATH = os.path.join(MUSIC_PATH, '.music.json')
ARTIST_DATABASE_PATH = os.path.join(MUSIC_PATH, '.artists.json')
TORRENTS_DATABASE_PATH = os.path.join(MUSIC_PATH, '.torrents.json')
TOP_QUALITY = ['flac', 'cd']

if not os.path.isfile(TORRENTS_PATH):
    os.system('mkdir %s' % TORRENTS_PATH)

def artistParser(artist_typed):

    assert type(artist_typed) is str, "artist is not a string: %r" % artist_typed

    artist_typed = artist_typed.lower()
    artist_html = artist_typed.replace(' ', '%20')

    return artist_typed, artist_html

def dateStrToDatetime(date):

    assert type(date) is str, "date is not a string object: %r" % date

    if len(date)==4:
        return datetime.fromtimestamp(mktime(strptime(date, '%Y')))
    elif len(date)==7:
        return datetime.fromtimestamp(mktime(strptime(date, '%Y-%m')))
    else:
        return datetime.fromtimestamp(mktime(strptime(date, '%Y-%m-%d')))

