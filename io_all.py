#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

DI0 = 17
DI1 = 27
DO0 = 23
DO1 = 24

GPIO.setup(DI0, GPIO.IN)
GPIO.setup(DI1, GPIO.IN)
GPIO.setup(DO0, GPIO.OUT)
GPIO.setup(DO1, GPIO.OUT)

try:
    while True:
        if GPIO.input(DI0):
            GPIO.output(DO0, 1)
        else:
            GPIO.output(DO0, 0)

        if GPIO.input(DI1):
            GPIO.output(DO1, 1)
        else:
            GPIO.output(DO1, 0)

        sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
