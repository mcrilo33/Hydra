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
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from utilities import artistParser, dateStrToDatetime, MUSIC_PATH, \
    TORRENTS_PATH, MUSIC_DATABASE_PATH, ARTIST_DATABASE_PATH, \
    TORRENTS_DATABASE_PATH
from musicBrainz import checkMusicBrainzReleaseGroup
from tinydb import TinyDB, Query

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

    assert type(content) is str, "content is not a string object: %r" % content

    torrent = bencode.bdecode(content)
    tree = itertools.chain((f["path"] for f in torrent["info"]["files"]))
    dirs = {t[0]:True for t in tree if len(t)>1}

    return torrent['info']['name'], dirs

def checkTorrentIsFromTheArtist(artist_id, content):

    assert type(artist__id) is str, "artist_id is not a string: %r" % artist_id
    assert type(content) is str, "content is not a string object: %r" % content

    torrent_name, torrent_dirs = getTorrentContent(content)
    for dir in torrent_dirs:
        if checkMusicBrainzReleaseGroup(artist_id, dir):
            return True
    if checkMusicBrainzReleaseGroup(artist_id, torrent_name):
        return True
    
    return False

def checkTorrent(artist_id, content):

    if not checkTorrentIsFromTheArtist(artist_id, content):
        return False
    if 
    
def getRuTrackerTorrents(artist_id, date):

    assert type(artist__id) is str, "artist_id is not a string: %r" % artist_id
    assert type(date) is str, "date is not a string object: %r" % date

    global TOP_LEVEL_URL
    global USERNAME
    global PASSWORD
        
    music_db = TinyDB(MUSIC_DATABASE_PATH)
    artist_db = TinyDB(ARTIST_DATABASE_PATH)
    artist = Query()
    artist_name = db.search(artist.artist-mbid == artist_id).artist-name
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
    response = req.post(
        login_url,
        data=post_data,
        timeout=60,
        stream=True,
        verify=False,
        headers=HEADERS
    )

    url = "https://rutracker.org/forum/tracker.php?nm=%s" % (artist)
    response = req.get(url, data=post_data, timeout=60, stream=True, verify=False, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('tr', class_='hl-tr')

    link_count = 0
    next = True
    torrent_db = TinyDB(TORRENTS_DATABASE_PATH)
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

            # Check if it has been already downloaded
            torrent = Query()
            results = torrent_db.search(
                torrent.hash == hash
            )
            if len(results)==0 and checkTorrent(artist_id, content):
                open(tmp_path, 'wb').write(response.content)
                torrent_db.insert({'hash': hash})
                link_count += 1

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

    return 0
