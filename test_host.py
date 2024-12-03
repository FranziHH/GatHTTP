#!/usr/bin/env python

import os

eth0 = os.popen('ip addr show eth0 | grep -vw "inet6" | grep "global" | grep -w "inet" | cut -d/ -f1 | awk \'{ print $2 }\'').read()
wlan0 = os.popen('ip addr show wlan0 | grep -vw "inet6" | grep "global" | grep -w "inet" | cut -d/ -f1 | awk \'{ print $2 }\'').read()

print(eth0)
