#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : tinydb.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 17.10.2018
# Last Modified Date: 17.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import datetime
from tinydb import TinyDB, Query
import pandas as pd
import os
from .musicBrainz import getMusicBrainzAlbums, getMusicBrainzArtistId
from .rutracker import getRuTrackerTorrents
from .utilities import MUSIC_DATABASE_PATH, ARTIST_DATABASE_PATH, \
    artistParser, TORRENTS_DATABASE_PATH, REJECTED_PATH, \
    TORRENTS_PATH

def addNewArtist(artist_typed, verbose=True):

    artist_typed, artist = artistParser(artist_typed)
    music_db = TinyDB(MUSIC_DATABASE_PATH)
    artist_db = TinyDB(ARTIST_DATABASE_PATH)
    torrent_db = TinyDB(TORRENTS_DATABASE_PATH)
    artist_id = getMusicBrainzArtistId(artist_typed)
    albums = getMusicBrainzAlbums(artist_id, '')

    # debug purpose
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

def downloadRejected(verbose=True):

    rejected_df = pd.read_csv(REJECTED_PATH)
    for i, row in rejected_df.iterrows():
        tmp_path = os.path.join(TORRENTS_PATH, row.hash + '.torrent')
        ask = True
        while(ask):
            print(
                'Torrent : {} has been rejected.\nReason : {}.'.format(
                    row.torrent_name,
                    row.reason
                )
            )
            answer = input('Do you want to download it yet ? (default:y|n)\n')
            if answer == '':
                answer = 'y'
            if answer in ['y', 'n']:
                ask = False
        if answer == 'y':
            os.system('transmission-daemon >&-')
            os.system('transmission-remote -a {} >&-'.format(tmp_path))
        else:
            if verbose:
                print('-> {} is deleted.\n'.format(row.torrent_name))
            os.system('rm {}'.format(tmp_path))
        rejected_df = rejected_df[rejected_df.index!=i]
        rejected_df.to_csv(REJECTED_PATH, index=False)
    if verbose:
        print('Rejected list cleaned.')
    os.system('rm {}'.format(REJECTED_PATH))

