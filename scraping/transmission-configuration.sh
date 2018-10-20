#!/bin/bash
# File              : scraping/transmission-configuration.sh
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 20.10.2018
# Last Modified Date: 20.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

# Set download options
transmission-remote --lpd >&- # Enable local peer discovery (LPD)
transmission-remote --pex >&- # Enable peer exchange (PEX)
transmission-remote --utp >&- # Enable uTP for peer connections
transmission-remote --no-trash-torrent >&- # Do not delete torrents after adding

root_path=$(cat .opt.txt)
# Set the default download folder
transmission-remote --download-dir "$root_path/finished" >&-
# Where to store new torrents until they're complete
transmission-remote --incomplete-dir "$root_path/download" >&-
#transmission-remote --torrent-done-script <file> # Necessary to process files after downloading
