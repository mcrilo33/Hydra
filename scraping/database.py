#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : tinydb.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 17.10.2018
# Last Modified Date: 17.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import datetime
from utilities import MUSIC_DATABASE_PATH, ARTIST_DATABASE_PATH, artistParser
from musicBrainz import getMusicBrainzAlbums, getMusicBrainzArtistId
from tinydb import TinyDB, Query

def addNewArtist(artist_typed):

    artist_typed, artist = artistParser(artist_typed)
    music_db = TinyDB(MUSIC_DATABASE_PATH)
    artist_db = TinyDB(ARTIST_DATABASE_PATH)
    artist_id = getMusicBrainzArtistId(artist_typed)
    albums = getMusicBrainzAlbums(artist_id, '')

    artist_db.insert({
        'artist-mbid': artist_id,
        'artist-name': artist_typed,
        'update-date': datetime.datetime.now().strftime('%Y-%m-%d')
    })
    for album in albums:
        music_db.insert({
            'artist-mbid': album[0],
            'date': album[1],
            'title': album[2],
            'release-group-mbid': album[3]
        })

    # trackers = getRuTrackerTorrents(artist_id, date)


addNewArtist('Aphex Twin')
