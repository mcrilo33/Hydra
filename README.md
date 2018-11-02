# Hydra

<img src="https://mcrilo33.github.io/Hydra/logo.svg" align="right"
     title="Hydra" width="100" height="100">

Hydra is a music manager written in python which keep all your music well organized and use popular p2p tracker to update and download music freely available on the web.

## Dependencies

* [<img src="https://mcrilo33.github.io/Hydra/transmission-logo.png" width="25" height="25"> Transmission-cli](https://transmissionbt.com/) as a light-weight and cross-platform BitTorrent client.
* [<img src="https://mcrilo33.github.io/Hydra/picard-logo.svg" width="25" height="25"> MusicBrainz Picard](https://picard.musicbrainz.org/) as a cross-platform music tagger.

## How It Works

Hydra tracks all torrents downloaded with transmission-cli and analyzes all your music files tagged with MusicBrainz Picard which gives a unique id for each of your albums. Thus it keeps only your best recordings and delete duplicates automatically.

Moreover, it has a downloading routine to keep track of all new music available on the web from your favorite artists.


## Installation

First, install `transmission-cli` and `picard`:

```sh
$ sudo apt-get install transmission-cli # for ubuntu
$ sudo apt-get install picard
```

Then clone the repo and make init :
```sh
$ git clone https://github.com/mcrilo33/Hydra.git && cd Hydra
$ make init
```
You can finally test if Hydra finds all the dependencies with :
```sh
$ make test
```

## Usage

If you followed the installation process accordingly everything should be working fine.
```sh
$ python main.py --help # Gives all available options
```

At first use you will need to give the path of your music library. It will create at this path a Downloads directory where transmission-cli will put files still downloading, a Finished directory to move downloaded files, and a Tagged directory where you can find your music properly tagged and organized (it's the final directory - you should see it as your Music Library directory).

Warning : To function properly, all files put in Tagged should be tagged with MusicBrainz Picard before.

If you want to add a new artist in your library :

```sh
# download all albums from this artist that Hydra can find.
$ python main.py --new "Name of your favorite artist"
```

When some files are downloaded you must tag it with MusicBrainz Picard.
You can look up at this [guide](https://picard.musicbrainz.org/quick-start/) if you don't know how to do it.

Finally you just have to enjoy your music organized in Tagged with the player of your choice. A good one I recommend is [Deadbeef](https://en.wikipedia.org/wiki/DeaDBeeF) which can give you bit perfect audio playback. Another one is [Google Play Music](https://play.google.com/music/) which is a music and podcast streaming service where you can put freely your own music up to 50.000 tracks.

## Suggestion
You might want to configure transmission-cli so that it launches at startup.

You migt also want to configure a cronjob with a command like this :
```sh
$(crontab -l ; echo "0 0 * * 0 python absolute/path/to/main.py --downloading")| crontab - 
```
To download new albums of the artists in the database regularly, every week for instance.
