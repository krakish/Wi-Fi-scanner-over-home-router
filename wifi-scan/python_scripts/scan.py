#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telnetlib
import time

while True:
    try:
        with open('config.txt', 'r') as conf:
            conf_text = conf.read()
            telnet_ip = conf_text.split('\n')[0].split('=')[1]
        tn = telnetlib.Telnet()
        tn.open(telnet_ip, 23, timeout=2)
        try:
                tn.read_until(b'F660V2.0\nLogin:', timeout=2)
                tn.write(b'root\n')
                tn.read_until(b'Password:', timeout=2)
                tn.write(b'root\n')
                tn.read_until(b'#', timeout=3)
                tn.write(b'wl monitor 1\n')
                tn.read_until(b'#', timeout=3)
                tn.write(b'wl scan\n')
                time.sleep(2)
                tn.read_until(b'#', timeout=3)
                tn.write(b'wl scanresults\n')
                res = tn.read_until(b'/ #', timeout=3).decode('utf-8')
                with open('scan_result.txt', 'w') as f:
                    f.write(res)
                    #print(res)
                tn.close()
                print('ok')
                time.sleep(3)
        except:
                print('not enough pty')
                time.sleep(1)
                pass
    except:
        print('n/a')
        with open('scan_result.txt', 'w') as f:
            f.write("")
            try:
                tn.close()
            except:
                pass
        time.sleep(1)


