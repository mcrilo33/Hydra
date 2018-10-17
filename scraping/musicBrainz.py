#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : musicbrainz.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 08.10.2018
# Last Modified Date: 08.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import urllib.request
import json
from datetime import datetime
from time import strptime

def dateStrToDatetime(date):
    assert type(date) is str, "date is not a string object: %r" % date
    if len(date)==4:
        return strptime(date, '%Y')
    elif len(date)==7:
        return strptime(date, '%Y-%m')
    else:
        return strptime(date, '%Y-%m-%d')

def getMusicBrainzAlbums(artist_typed, date):

    assert type(artist_typed) is str, "artist is not a string: %r" % artist_typed
    assert type(date) is str, "date is not a string object: %r" % date

    albums = []
    artist_typed = artist_typed.lower()
    artist = artist_typed.replace(' ', '%20')
    date = dateStrToDatetime(date)

    # get MusicBrainz id
    url = """
        http://musicbrainz.org/ws/2/artist/?query=%s&fmt=json
    """ % (artist)
    response = (urllib.request.urlopen(url)).read()
    data = json.loads(response)
    id = data['artists'][0]['id']

    # get albums list
    url = """
        https://musicbrainz.org/ws/2/release-group?artist=%s&fmt=json&limit=100
    """ % (id)
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
        print(album)
        album_date = album['first-release-date']
        if album_date!='':
            album_date_tmp =  dateStrToDatetime(album_date)
        if album_date=='' or (date and date <= album_date_tmp):
            results.append((artist, album_date, album['title'], album['id']))

    return results

res = getMusicBrainzAlbums('andrea parker', '1000')
print(res)
print(len(res))
