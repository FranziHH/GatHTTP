#!/usr/bin/env python

import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep             # lets us have a delay
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
DO0 = 23
DO1 = 24

GPIO.setup(DO0, GPIO.OUT)
GPIO.setup(DO1, GPIO.OUT)

try:
    while True:
        GPIO.output(DO0, 1)
        GPIO.output(DO1, 0)
        sleep(0.5)
        GPIO.output(DO0, 0)
        GPIO.output(DO1, 1)
        sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
