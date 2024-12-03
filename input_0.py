#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep     # this lets us have a time delay (see line 12)
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering

DI0 = 17
DI1 = 27

GPIO.setup(DI0, GPIO.IN)    # set GPIO 17 as input
# GPIO.setup(DI1, GPIO.IN)    # set GPIO 27 as input

try:
    while True:            # this will carry on until you hit CTRL+C
        if GPIO.input(DI0): # if port 17 == 1
            print("DI0 - ON")
        else:
            print("DI0 - OFF")

        # if GPIO.input(DI1): # if port 27 == 1
        #    print("DI1 - ON")
        # else:
        #    print("DI1 - OFF")

        sleep(0.1)         # wait 0.1 seconds

except KeyboardInterrupt:
    GPIO.cleanup()         # clean up after yourself
