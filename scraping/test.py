#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : scraping/test.py
# Author            : Mathieu Crilout <mathieucrilout@mail>
# Date              : 20.10.2018
# Last Modified Date: 20.10.2018
# Last Modified By  : Mathieu Crilout <mathieucrilout@mail>

import subprocess

def test():

    proc = subprocess.Popen(["command -v transmission-remote"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    proc = subprocess.Popen(["command -v transmission-daemon"], stdout=subprocess.PIPE, shell=True)
    (out2, err2) = proc.communicate()

    if out == '' or out2 == '':
        raise ValueError(
            "To function properly Hydra needs transmission-cli.\n"\
            + "transmission-cli isn't properly installed.\n"\
            + "You need to (re)install it."
        )
    else:
        print('transmission-cli installed properly =================================== [success]')
