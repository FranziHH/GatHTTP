#!/usr/bin/env python

# if you gets error like "usr/bin/env: ‘python\r’: No such file or directory"
# convert file from dos into unix: "dos2unix [filename]"

from func_relais import *
import time

# All Off
RelaisOff(1, 255)
time.sleep(0.5)

try:
    while True:
        for i in range(8):
            print ("Relais On: #" + str(i))
            RelaisOn(1, i)
            time.sleep(0.5)

        for i in range(8):
            print ("Relais Off: #" + str(i))
            RelaisOff(1, i)
            time.sleep(0.5)

except KeyboardInterrupt:
    pass

RelaisOff(1, 255)

