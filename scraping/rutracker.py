#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : rutracker.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 16.10.2018
# Last Modified Date: 16.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import dateparser
import requests_html
import hashlib
import os
import datetime
import time
import bencode
import itertools
import pandas as pd

from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from .utilities import artistParser, dateStrToDatetime, MUSIC_PATH, \
    TORRENTS_PATH, MUSIC_DATABASE_PATH, ARTIST_DATABASE_PATH, \
    TORRENTS_DATABASE_PATH, REJECTED_PATH
from .musicBrainz import checkMusicBrainzReleaseGroup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOP_LEVEL_URL = 'https://rutracker.org'
USERNAME = 'dieu783'
PASSWORD = 'penlat16rch'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'close',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

def getTorrentContent(content):

    torrent = bencode.bdecode(content)

    if "files" not in torrent["info"]:
        if os.path.splitext(torrent["info"]["name"])[1]:
            return torrent['info']['name'], [], False
        print('{} rejected !'.format(torrent["info"]["name"]))
        return '', [], True

    tree = itertools.chain((f["path"] for f in torrent["info"]["files"]))
    dirs = {t[0]:True for t in tree if len(t)>1}


    return torrent['info']['name'], dirs, False

def checkTorrentIsFromTheArtist(artist_id, torrent_name, torrent_dirs):

    reasons = {}
    for dir in torrent_dirs:
        test, reason = checkMusicBrainzReleaseGroup(artist_id, dir)
        if test:
            return True, ''
    test, reason = checkMusicBrainzReleaseGroup(artist_id, torrent_name)
    if test:
        return True, ''
    else:
        return False, reason

def saveRejected(torrent_name, reason, hash):

    if os.path.isfile(REJECTED_PATH):
        rejected_df = pd.read_csv(REJECTED_PATH)
    else:
        rejected_df = pd.DataFrame(
            [],
            columns=['torrent_name', 'reason', 'hash']
        )

    tmp = pd.DataFrame(
            [[torrent_name, reason, hash]],
            columns=['torrent_name', 'reason', 'hash']
        )
    rejected_df = rejected_df.append(tmp)
    rejected_df.to_csv(REJECTED_PATH, index=False)

def checkTorrent(artist_id, hash, content, torrent_db, tmp_path, verbose=True):

    torrent_name, torrent_dirs, exception = getTorrentContent(content)

    test, reason = True, ''
    if exception:
        test, reason = False, 'Bad name format.'

    if test:
        test, reason = checkTorrentIsFromTheArtist(artist_id, torrent_name, torrent_dirs)
    if test:
        # Check if it has already been downloaded
        torrent = Query()
        results = torrent_db.search(
            torrent.hash == hash
        )
        if len(results)>0:
            test, reason = False, 'It has already been downloaded.'

    if test:
        if verbose:
            print(
                'New torrent : {} is added to the database.'.format(torrent_name)
            )
    else:
        if verbose:
            print(
                'New torrent : {} is rejected.\nReason : {}.'.format(
                    torrent_name,
                    reason
                )
            )
        if reason != "It's not a music file.":
            saveRejected(torrent_name, reason, hash)

    open(tmp_path, 'wb').write(content)
    torrent_db.insert({'hash': hash})

    return test, reason
    
def getRuTrackerTorrents(artist_id, date, verbose=True):

    assert type(artist_id) is str, "artist_id is not a string: %r" % artist_id
    assert type(date) is str, "date is not a string object: %r" % date

    global TOP_LEVEL_URL
    global USERNAME
    global PASSWORD
        
    music_db = TinyDB(MUSIC_DATABASE_PATH)
    artist_db = TinyDB(ARTIST_DATABASE_PATH)
    artist = Query()
    artist_name = artist_db.search(
        artist.artist_mbid == artist_id
    )[0]['artist_name']
    artist_name, artist = artistParser(artist_name)
    if date != '':
       date = dateStrToDatetime(date)

    # CONNECT TO RUTRACKER
    req = requests_html.HTMLSession()
    login_url = 'https://rutracker.org/forum/login.php'
    post_data = {
        'login_username': USERNAME,
        'login_password': PASSWORD,
        'login': 'вход',
    }
    connected = False
    while not connected:
        try:
            response = req.post(
                login_url,
                data=post_data,
                timeout=10,
                stream=True,
                verify=False,
                headers=HEADERS
            )
            connected = True
        except:
            connected = False
    if verbose:
        print('Connected at RuTracker.org...\n')

    url = "https://rutracker.org/forum/tracker.php?nm=%s" % (artist)
    connected = False
    while not connected:
        try:
            response = req.get(
                url,
                data=post_data,
                timeout=10,
                stream=True,
                verify=False,
                headers=HEADERS
            )
            connected = True
        except:
            connected = False
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('tr', class_='hl-tr')

    link_count = 0
    next = True
    torrent_db = TinyDB(TORRENTS_DATABASE_PATH)
    if verbose:
        print('Starting to download torrents ' \
            + 'related to {}...\n'.format(artist_name.upper()))
        start_time = time.time()
    while(next):
        for link in links:
            date_tmp = link.find('p').text
            date_tmp = dateparser.parse(date_tmp, languages=['ru'])
            torrent_link = link.find('a', class_='dl-stub').get('href')
            response = req.get(
                TOP_LEVEL_URL + '/forum/' + torrent_link,
                allow_redirects=True
            )

            hash = hashlib.md5(response.content).hexdigest()
            tmp_path = os.path.join(TORRENTS_PATH, hash + '.torrent')

            test, reason = checkTorrent(artist_id,
                            hash,
                            response.content,
                            torrent_db,
                            tmp_path,
                            verbose=verbose)
            if test:
                os.system('transmission-daemon')
                os.system('transmission-remote -a {}'.format(tmp_path))
                link_count += 1
                if verbose:
                    print('Total downloaded : {}'.format(link_count))
            else:
                if verbose:
                    print('Total downloaded : {}'.format(link_count))

            if (link_count>500
                or (link_count>200 and datetime.datetime(2010, 1, 1) > date_tmp)
                or (date != '' and date > date_tmp)):
                return 0

        next_button = soup.find('a', text='След.')
        if next_button != None:
            next_url = next_button.get('href')
            response = req.get(
                TOP_LEVEL_URL + '/forum/' + next_url,
                data=post_data,
                timeout=60,
                stream=True,
                verify=False,
                headers=HEADERS
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('tr', class_='hl-tr')
        else:
            next = False

    if verbose:
        print('Downloading done. Took {:10.2f}s'.format(time.time() - start_time))

        rejected_df = pd.read_csv(REJECTED_PATH)
        for i, row in rejected_df.iterrows():
            print(
                'New torrent : {} is rejected.\nReason : {}.'.format(
                    row.torrent_name,
                    row.reason
                )
            )
    return 0

