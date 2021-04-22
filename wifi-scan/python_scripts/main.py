#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import time



if __name__ == '__main__':
    gui = subprocess.Popen(['python3', 'gui.py'])
    pid_gui = gui.pid
    scan = subprocess.Popen(['python3', 'scan.py'])
    pid_scan = scan.pid
    ping = subprocess.Popen(['python3', 'ping.py'])
    pid_ping = ping.pid

    while True:
        if gui.poll() is not None or scan.poll() is not None or ping.poll() is not None:
            try:
                scan.terminate()
            except:
                pass
            try:
                gui.terminate()
            except:
                pass
            try:
                ping.terminate()
            except:
                pass
            exit(1)
        time.sleep(1)


