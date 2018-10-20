# Hydra
Hydra is a music manager which keep all your music well organized and use popular p2p tracker to update and download music.

**Already working**

python main.py --new "Name of an artist"

Add an artist to the Hydra database and then download from rutracker all the
revelant torrents from this artist.

python main.py --rejected

Wether to download or not ambiguous rejected torrents.

**Coming soon**:

After torrent has been download automatically format it well.

Check on a week basis, wether or not, our artists in Hydra database have new
albums to download.

## Installation

### Dependencies

Hydra uses transmission-cli to download all torrents. You need to install it.

For ubuntu the command is : >>sudo apt-get install transmission-cli

For arch with pacman manager the command is : >>sudo pacman -S transmission-cli
Etc...

### User Installation

No installer.
