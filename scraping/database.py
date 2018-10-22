#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : tinydb.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 17.10.2018
# Last Modified Date: 17.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import datetime
import pandas as pd
import os
import re
from tinydb import TinyDB, Query
from .musicBrainz import getMusicBrainzAlbums, getMusicBrainzArtistId
from .rutracker import getRuTrackerTorrents
from .utilities import MUSIC_DATABASE_PATH, ARTIST_DATABASE_PATH, \
    artistParser, TORRENTS_DATABASE_PATH, REJECTED_PATH, \
    TORRENTS_PATH

AUDIO_TYPE = [
    '.riff',
    '.wav',
    '.bwf',
    '.ogg',
    '.aiff',
    '.caf',
    '.raw',
    '.flac',
    '.alac',
    '.ac-3',
    '.mp3',
    '.ogg'
]
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
            'release_group_mbid': album[3],
            'bitrate': 0,
            'path': ''
        })
        if verbose:
            print('Album : {:<46.46} inserted in database.'.format('"'+album[2]+'"'))
    if verbose:
        print('Total Albums added : {}'.format(len(albums)) \
            + ' ====================================================\n')

    getRuTrackerTorrents(artist_id, '', verbose=verbose)
    return 0

def downloadRejected(verbose=True):

    if not os.path.isfile(REJECTED_PATH):
        print('[Hydra] There is no rejected torrents to processed.')
        return 0
    rejected_df = pd.read_csv(REJECTED_PATH)
    print('[Hydra] Rejected list :')
    for i, row in rejected_df.iterrows():
        print('        {}'.format(row.torrent_name))
        print('        {}'.format(row.rutracker_link))
    for i, row in rejected_df.iterrows():
        tmp_path = os.path.join(TORRENTS_PATH, row.hash + '.torrent')
        ask = True
        while(ask):
            print(
                '[Hydra] Torrent : {} has been rejected.\n[Hydra] Reason : {}'.format(
                    row.torrent_name,
                    row.reason
                )
            )
            answer = input('Hydra : Do you want to download it yet ? (default:y|n)\n')
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
        print('[Hydra] Rejected list cleaned.')
    os.system('rm {}'.format(REJECTED_PATH))

    return 0

def updateDatabase():

    with open('.opt.txt') as f:
        root = f.read() + '/tagged'
    walk = list(os.walk(root))
    for w in walk:
        for file in w[2]:
            if os.path.splitext(file)[1] in AUDIO_TYPE:
                path = os.path.join(w[0], file)
                updateAlbum(path)
            break

def updateAlbum(path):
    path = re.sub(' ', '\\ ', path)
    print(path)
    command = "ffprobe {} &> .tmp.txt".format(path)
    os.system(command)

    with open('.tmp.txt') as f:
        ffprobe_result = f.read()

    try:
        artist_mbid = re.search(
            'musicbrainz_artistid\s*: (.*)\n',
            ffprobe_result,
            flags=re.IGNORECASE
        ).group(1)
        date = re.search(
            'date\s*: (.*)\n',
            ffprobe_result,
            flags=re.IGNORECASE
        ).group(1)
        title = re.search(
            'album\s*: (.*)\n',
            ffprobe_result,
            flags=re.IGNORECASE
        ).group(1)
        release_group_mbid = re.search(
            'musicbrainz_releasegroupid\s*: (.*)\n',
            ffprobe_result,
            flags=re.IGNORECASE
        ).group(1)
        bitrate = int(re.search(
            'bitrate: (\d+)',
            ffprobe_result,
            flags=re.IGNORECASE
        ).group(1))
    except:
        print('[Hydra] Warning : {} is badly tagged !\n'.format(
            os.path.dirname(path)) \
              + '        You should edit it manually.')
        return 1

    print(
        artist_mbid+'\n',
        date+'\n',
        title+'\n',
        release_group_mbid+'\n',
        bitrate,
        path
    )
    music_db = TinyDB(ARTIST_DATABASE_PATH)
    albums = Query()
    album_query = music_db.search(
        albums.release_group_mbid == release_group_mbid
    )
    # if album is better than the older one
    if (len(album_query) > 0 and album_query[0]['bitrate'] < bitrate):
        # delete the older one
        os.system('rm -rf {}'.format(album_query[0]['path']))
        print(path)
        path = re.sub('\\\\ ', ' ', path)
        path = os.path.dirname(path)
        path = re.sub(' ', '\\ ', path)
        better = True
        album_query = music_db.update(
            {
                'artist_mbid': artist_mbid,
                'date': date,
                'title': title,
                'release_group_mbid': release_group_mbid,
                'bitrate': bitrate,
                'path': os.path.dirname(path)
            },
            albums.release_group_mbid == release_group_mbid
        )
    if len(album_query) == 0:
        album_query = music_db.insert(
            {
                'artist_mbid': artist_mbid,
                'date': date,
                'title': title,
                'release_group_mbid': release_group_mbid,
                'bitrate': bitrate,
                'path': os.path.dirname(path)
            }
        )

    return 0
