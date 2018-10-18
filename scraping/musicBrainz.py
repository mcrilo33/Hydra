#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : musicbrainz.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 08.10.2018
# Last Modified Date: 08.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import urllib.request
import json
import re
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from tinydb import TinyDB, Query
from .utilities import artistParser, dateStrToDatetime, \
    MUSIC_DATABASE_PATH, TOP_QUALITY

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts = urllib.parse.urlparse(iri)
    return urllib.parse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

def getMusicBrainzArtistId(artist_typed):
    assert type(artist_typed) is str, "artist is not a string: %r" % artist_typed

    artist_typed, artist = artistParser(artist_typed)
    # get MusicBrainz id
    url = """
        http://musicbrainz.org/ws/2/artist/?query=%s&fmt=json
    """ % (artist)
    url = re.sub(r'[^\x00-\x7f]',r'', url)
    response = (urllib.request.urlopen(url)).read()
    data = json.loads(response)
    id = data['artists'][0]['id']

    return id

def getMusicBrainzAlbums(artist_id, date):

    assert type(artist_id) is str, "artist_id is not a string: %r" % artist_typed
    assert type(date) is str, "date is not a string object: %r" % date

    albums = []
    if date != '':
        date = dateStrToDatetime(date)

    # get albums list
    url = """
        https://musicbrainz.org/ws/2/release-group?artist=%s&fmt=json&limit=100
    """ % (artist_id)
    response = (urllib.request.urlopen(url)).read()
    data = json.loads(response)
    total = data['release-group-count']
    releases = data['release-groups']
    local_count = 0
    count = 0
    while(count!=total):
        if local_count==len(releases):
            url = """
                https://musicbrainz.org/ws/2/release-group?artist=%s&fmt=json&limit=100&offset=%s
            """ % (id, count)
            response = (urllib.request.urlopen(url)).read()
            data = json.loads(response)
            releases = data['release-groups']
            local_count = 0
        albums.append(releases[local_count])
        local_count += 1
        count += 1

    results = []
    for album in albums:
        album_date = album['first-release-date']
        if album_date!='':
            album_date_tmp =  dateStrToDatetime(album_date)
        if album_date=='' or (date != '' and date <= album_date_tmp):
            results.append((artist_id, album_date, album['title'], album['id']))

    return results

def checkMusicBrainzReleaseGroup(artist_id, title_typed):

    assert type(artist_id) is str, "artist_id is not a string: %r" % artist_id
    assert type(title_typed) is str, "title is not a string: %r" % title_typed

    title_typed , title = artistParser(title_typed)

    # get MusicBrainz release-group infos
    url = \
        'http://musicbrainz.org/ws/2/release-group/?query=release:{}%20AND%20arid:{}'.format(
        title,
        artist_id
    )

    url = re.sub(r'[^\x00-\x7f]',r'', url)
    response = (urllib.request.urlopen(url)).read()
    os.system('sleep 1')
    data = ET.fromstring(response)

    # Check if there is corresponding release-group
    if len(data[0])>0:
        # Then check if we already have a good copy
        music_db = TinyDB(MUSIC_DATABASE_PATH)
        release = Query()
        results = music_db.search(
            release.release_group_mbid == data[0][0].get('id')
        )
        if(len(results) == 0
           or not ('quality' in results[0] and results[0]['quality'] in
                TOP_QUALITY)):
            return True

    return False

