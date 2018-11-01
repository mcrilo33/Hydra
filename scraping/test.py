#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : scraping/test.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 20.10.2018
# Last Modified Date: 20.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import subprocess
import os

def testAuto():

    proc = subprocess.Popen(["command -v transmission-remote"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    proc = subprocess.Popen(["command -v transmission-daemon"], stdout=subprocess.PIPE, shell=True)
    (out2, err2) = proc.communicate()

    if out == '' or out2 == '':
        raise ValueError(
            "[Hydra] To function properly Hydra needs transmission-cli.\n"\
            + "        transmission-cli isn't properly installed.\n"\
            + "        You need to (re)install it."
        )
    else:
        print('[Hydra] transmission-cli installed properly =================================== [success]')

    proc = subprocess.Popen(["command -v picard"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    if out == '':
        raise ValueError(
            "[Hydra] To function properly Hydra needs MusicBrainz Picard.\n"\
            + "        https://picard.musicbrainz.org/\n"\
            + "        MusicBrainz Picard isn't properly installed.\n"\
            + "        You need to (re)install it."
        )
    else:
        print('[Hydra] MusicBrainz Picard is installed properly =================================== [success]')

def setPicardSetting(path):

    proc = subprocess.Popen(["echo $HOME"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    picard_path = out.decode()[:-1] + '/.config/MusicBrainz/Picard.ini'
    with open(picard_path, 'r') as f:
        picard_config = f.read()
    if re.search('file_naming_format', picard_config):
        picard_config = re.sub(
            'file_naming_format=.*\n',
            'file_naming_format="$if(%genre%, %genre%/)$if2(%albumartist%,%artist%)/$if(%date%, %date% - )$if($ne(%albumartist%,),%album%/,)$if($gt(%totaldiscs%,1),%discnumber%-,)$if($ne(%albumartist%,),$num(%tracknumber%,2) ,)$if(%_multiartist%,%artist% - ,)%title%"\n',
            picard_config
        )
    else:
        picard_config = re.sub(
            '\[setting\]\n',
            '[setting]\nfile_naming_format="$if(%genre%, %genre%/)$if2(%albumartist%,%artist%)/$if(%date%, %date% - )$if($ne(%albumartist%,),%album%/,)$if($gt(%totaldiscs%,1),%discnumber%-,)$if($ne(%albumartist%,),$num(%tracknumber%,2) ,)$if(%_multiartist%,%artist% - ,)%title%"\n',
            picard_config
        )
    if re.search('move_files=', picard_config):
        picard_config = re.sub(
            'move_files=.*\n',
            'move_files=true\n',
            picard_config
        )
    else:
        picard_config = re.sub(
            '\[setting\]\n',
            '[setting]\nmove_files=true\n',
            picard_config
        )
    if re.search('rename_files=', picard_config):
        picard_config = re.sub(
            'rename_files=.*\n',
            'rename_files=true\n',
            picard_config
        )
    else:
        picard_config = re.sub(
            '\[setting\]\n',
            '[setting]\nrename_files=true\n',
            picard_config
        )
    if re.search('delete_empty_dirs=', picard_config):
        picard_config = re.sub(
            'delete_empty_dirs=.*\n',
            'delete_empty_dirs=true\n',
            picard_config
        )
    else:
        picard_config = re.sub(
            '\[setting\]\n',
            '[setting]\ndelete_empty_dirs=true\n',
            picard_config
        )
    if re.search('move_additional_files=', picard_config):
        picard_config = re.sub(
            'move_additional_files=.*\n',
            'move_additional_files=true\n',
            picard_config
        )
    else:
        picard_config = re.sub(
            '\[setting\]\n',
            '[setting]\nmove_additional_files=true\n',
            picard_config
        )
    if re.search('move_additional_files_pattern=', picard_config):
        picard_config = re.sub(
            'move_additional_files_pattern=.*\n',
            'move_additional_files_pattern=*\n',
            picard_config
        )
    else:
        picard_config = re.sub(
            '\[setting\]\n',
            '[setting]\nmove_additional_files_pattern=*\n',
            picard_config
        )
    if re.search('move_files_to=', picard_config):
        picard_config = re.sub(
            'move_files_to=.*\n',
            'move_files_to=' + path + '/tagged\n',
            picard_config
        )
    else:
        picard_config = re.sub(
            '\[setting\]\n',
            '[setting]\nmove_files_to=' + path + '/tagged\n',
            picard_config
        )
    if re.search('current_directory=', picard_config):
        picard_config = re.sub(
            'current_directory=.*\n',
            'current_directory=' + path + '/finished\n',
            picard_config
        )
        with open(picard_path, 'w') as f:
           f.write(picard_config)
    elif re.search('\[persist\]', picard_config):
        picard_config = re.sub(
            '\[persist\]\n',
            '[persist]\ncurrent_directory=' + path + '/finished\n',
            picard_config
        )
        with open(picard_path, 'w') as f:
           f.write(picard_config)
    else:
        with open(picard_path, 'w') as f:
            f.write(picard_config)
        with open(picard_path, 'a') as f:
            f.write('\n[persist]\ncurrent_directory=' + path + '/finished\n')
    print("[Hydra] MusicBrainz Picard options for Hydra have been set.")

def updateOptions():

    with open('.opt.txt', 'r') as f:
        path = f.read()

    if not os.path.isdir(path+'/downloads'):
        os.system('mkdir {}'.format(path+'/downloads'))
    if not os.path.isdir(path+'/finished'):
        os.system('mkdir {}'.format(path+'/finished'))
    if not os.path.isdir(path+'/tagged'):
        os.system('mkdir {}'.format(path+'/tagged'))
    os.system('./scraping/transmission-configuration.sh')
    os.system('./scraping/cron-job.sh')

