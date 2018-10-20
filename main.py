#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : main.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 08.10.2018
# Last Modified Date: 08.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import os
from scraping.database import addNewArtist, downloadRejected
from optparse import OptionParser
from scraping.test import test

DEFAULT_ROOT_PATH = '~/hydra-music'

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option(
        "-n", "--new",
        type="string",
        dest="artist_typed",
        default="",
        help="Name of the new artist to add in the Hydra database" \
          + " and to plug to the Hydra downloading routine."
    )
    parser.add_option(
        "-v", "--verbose",
        dest="verbose",
        default=True,
        help="Verbosity"
    )
    parser.add_option(
        "-r", "--rejected",
        dest="rejected",
        default=False,
        action="store_true",
        help="Routine to download or not rejected torrents."
    )
    parser.add_option(
        "-t", "--test",
        dest="test",
        default=False,
        action="store_true",
        help="Test procedure"
    )
    parser.add_option(
        "-b", "--base-path",
        dest="base_path",
        help="Set the path where Hydra will store your music."
    )
    (options, args) = parser.parse_args()

if not os.path.isfile('.opt.txt'):
    unspecified = True
    while unspecified:
        answer = input(
            "The root path where Hydra will store all your music hasn't been set.\n"\
            + "Specify an absolute path : (default : " + DEFAULT_ROOT_PATH + ")"
        )
        if answer == '':
            path = DEFAULT_ROOT_PATH
            os.system('mkdir {}'.format(path))
        else:
            path = answer
        if not os.path.isdir(path):
            print('Error, wrong directory specified : {}')
        else:
            unspecified = False
    with open('.opt.txt', 'w') as f:
        f.write(path)
    if not os.path.isdir(path+'/download'):
        os.system('mkdir {}'.format(path+'/downloads'))
    if not os.path.isdir(path+'/finished'):
        os.system('mkdir {}'.format(path+'/finished'))
    os.system('./scraping/transmission-configuration.sh')

artist_typed = options.artist_typed
rejected = options.rejected
verbose = options.verbose
base_path = options.base_path

if base_path:
    with open('.opt.txt', 'r') as f:
        old_path = f.read()
    if not os.path.isdir(base_path):
        raise ValueError('Error, wrong directory specified : {}')
    print(
        "Root path where Hydra store all your music has been changed :\n"\
        + base_path
        + "\nAll your data will be moved to the new path."
    )
    if not old_path == base_path:
        os.system('mv {}/.[!.]* {}'.format(old_path, base_path))
        with open('.opt.txt', 'w') as f:
            f.write(base_path)
        if not os.path.isdir(base_path+'/download'):
            os.system('mkdir {}'.format(base_path+'/downloads'))
        if not os.path.isdir(base_path+'/finished'):
            os.system('mkdir {}'.format(base_path+'/finished'))
        os.system('./scraping/transmission-configuration.sh')
elif artist_typed != '':
    addNewArtist(artist_typed, verbose=verbose)
elif rejected:
    downloadRejected(verbose=verbose)
elif test:
    test()
