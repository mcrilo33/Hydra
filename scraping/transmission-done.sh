#!/bin/bash
# File              : scraping/transmission-done.sh
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 21.10.2018
# Last Modified Date: 21.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

TR_TORRENT_DIR=${TR_TORRENT_DIR:-$1}
TR_TORRENT_NAME=${TR_TORRENT_NAME:-$2}
TR_TORRENT_ID=${TR_TORRENT_ID:-$3}
destinationPath="/media/7f2d80ba-2a7c-4708-b601-673b304243fa/MySeries/"
transmission-remote -t "${TR_TORRENT_ID}" --move "${destinationPath}"
