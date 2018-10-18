#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : tinydb.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 17.10.2018
# Last Modified Date: 17.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import datetime
from tinydb import TinyDB, Query
from .musicBrainz import getMusicBrainzAlbums, getMusicBrainzArtistId
from .rutracker import getRuTrackerTorrents
from .utilities import MUSIC_DATABASE_PATH, ARTIST_DATABASE_PATH, \
    artistParser, TORRENTS_DATABASE_PATH

def addNewArtist(artist_typed, verbose=True):

    artist_typed, artist = artistParser(artist_typed)
    music_db = TinyDB(MUSIC_DATABASE_PATH)
    artist_db = TinyDB(ARTIST_DATABASE_PATH)
    torrent_db = TinyDB(TORRENTS_DATABASE_PATH)
    artist_id = getMusicBrainzArtistId(artist_typed)
    albums = getMusicBrainzAlbums(artist_id, '')

    music_db.purge()
    artist_db.purge()
    torrent_db.purge()
    test = Query()
    artists_query = artist_db.search(test.artist_mbid == artist_id)
    if len(artists_query) != 0:
        if verbose:
            print('Artist : {} already in database.'.format(artist_typed))
        return 0
    
    artist_db.insert({
        'artist_mbid': artist_id,
        'artist_name': artist_typed,
        'update_date': datetime.datetime.now().strftime('%Y-%m-%d')
    })
    if verbose:
        print('Artist : {} inserted in database.'.format(artist_typed.upper()))
    for album in albums:
        music_db.insert({
            'artist_mbid': album[0],
            'date': album[1],
            'title': album[2],
            'release_group_mbid': album[3]
        })
        if verbose:
            print('Album : {:<46.46} inserted in database.'.format('"'+album[2]+'"'))
    if verbose:
        print('Total Albums added : {}'.format(len(albums)) \
            + ' ====================================================\n')

    getRuTrackerTorrents(artist_id, '', verbose=verbose)
    return 0

