#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : utilities.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 17.10.2018
# Last Modified Date: 17.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import os
import re
from time import strptime, mktime
from datetime import datetime

with open('.opt.txt', 'r') as f:
    MUSIC_PATH = f.read()
TORRENTS_PATH = os.path.join(MUSIC_PATH, '.torrents')
MUSIC_DATABASE_PATH = os.path.join(MUSIC_PATH, '.music.json')
ARTIST_DATABASE_PATH = os.path.join(MUSIC_PATH, '.artists.json')
TORRENTS_DATABASE_PATH = os.path.join(MUSIC_PATH, '.torrents.json')
REJECTED_PATH = os.path.join(MUSIC_PATH, '.rejected.csv')
TOP_QUALITY = ['flac', 'cd']

if not os.path.isdir(TORRENTS_PATH):
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

def album_parsing(title):

    title = title.lower()
    title = re.sub(r'\([^\)]*\)', '', title)
    title = re.sub(r'\[[^\]]*\]', '', title)
    title = re.sub(r'\{[^\}]*\}', '', title)
    title = re.sub(r'\.\S+$', '', title)
    title = re.sub(r'(^| )(cassette|cd|ep|,)( |$)', r'\1\3', title)
    title = re.sub(r'(^| )((part|vol|disc) [I|1|2|3]+)( |$)', r'\1\3', title)
    title = re.sub(r'-|\.|&', ' ', title)
    title = re.sub(r'_', ' ', title)
    title = re.sub(r'\d{4}-\d{2}-\d{2}:?', ' ', title)
    title = re.sub(r'\d{4}', ' ', title)
    title = re.sub(r'[ ]+', ' ', title)
    title = re.sub(r'^[ ]+', '', title)
    title = re.sub(r'[ ]+$', '', title)

    return title
