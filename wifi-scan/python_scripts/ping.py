#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time

while True:
    with open('config.txt', 'r') as conf:
        conf_text = conf.read()
        ip = conf_text.split('\n')[1].split('=')[1]

    response = subprocess.run(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, universal_newlines=False)
    #print(response)
    time.sleep(3)