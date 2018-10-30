#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : main.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 08.10.2018
# Last Modified Date: 08.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import os
import subprocess
import re
from scraping.database import addNewArtist, downloadRejected, \
    updateDatabase, downloadingRoutine
from optparse import OptionParser
from scraping.test import testAuto, setPicardSetting

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
        "-b", "--base-path",
        dest="base_path",
        help="Set the path where Hydra will store your music."
    )
    parser.add_option(
        "-d", "--downloading",
        dest="downloading_routine",
        default=False,
        action="store_true",
        help="Launch the downloading routine. Best use is with cron job."
    )
    (options, args) = parser.parse_args()

    testAuto()
    # sett all options
    if os.path.isfile('.opt.txt'):
        with open('.opt.txt', 'r') as f:
            path = f.read()
    if not os.path.isfile('.opt.txt') or not os.path.isdir(path):
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
            if not os.path.isdir(path) or path[0] != '/':
                print('[Hydra] Error, wrong directory specified : {}'.format(path))
            else:
                unspecified = False
        with open('.opt.txt', 'w') as f:
            f.write(path)

    with open('.opt.txt', 'r') as f:
        path = f.read()

    if not os.path.isdir(path+'/downloads'):
        os.system('mkdir {}'.format(path+'/downloads'))
    if not os.path.isdir(path+'/finished'):
        os.system('mkdir {}'.format(path+'/finished'))
    if not os.path.isdir(path+'/tagged'):
        os.system('mkdir {}'.format(path+'/tagged'))

    os.system('./scraping/transmission-configuration.sh')

    # main
    artist_typed = options.artist_typed
    rejected = options.rejected
    verbose = options.verbose
    base_path = options.base_path
    downloading_routine = options.downloading_routine

    if base_path:
        with open('.opt.txt', 'r') as f:
            old_path = f.read()
        if not os.path.isdir(base_path) or base_path[0] != '/':
            raise ValueError('Error, wrong directory specified : {}'.format(base_path))
        print(
            "[Hydra] Root path where Hydra store all your music has been changed :\n"\
            + '        ' + base_path
            + "\n'        All your data will be moved to the new path."
        )
        if not old_path == base_path:
            os.system('mv {}/.[!.]* {}'.format(old_path, base_path))
            with open('.opt.txt', 'w') as f:
                f.write(base_path)
            if not os.path.isdir(base_path+'/downloads'):
                os.system('mkdir {}'.format(base_path+'/downloads'))
            if not os.path.isdir(base_path+'/finished'):
                os.system('mkdir {}'.format(base_path+'/finished'))
            if not os.path.isdir(base_path+'/tagged'):
                os.system('mkdir {}'.format(path+'/tagged'))
            os.system('./scraping/transmission-configuration.sh')
    elif artist_typed != '':
        os.system('./scraping/transmission-configuration.sh')
        updateDatabase()
        addNewArtist(artist_typed, verbose=verbose)
    elif rejected:
        os.system('./scraping/transmission-configuration.sh')
        downloadRejected(verbose=verbose)
    elif downloading_routine:
        #updateDatabase()
        downloadingRoutine()
