#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : main.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 08.10.2018
# Last Modified Date: 08.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

from scraping.database import addNewArtist
from optparse import OptionParser

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
    (options, args) = parser.parse_args()
    print(options, args)

artist_typed = options.artist_typed
verbose = options.verbose

if artist_typed != '':
    addNewArtist(artist_typed, verbose=verbose)

