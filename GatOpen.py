#!/usr/bin/env python

import sys
import configparser
import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep             # lets us have a delay

try:
    out = int(sys.argv[1])
except:
    out = 0  # red light

# Set Output GPIOs
DO0 = 23
DO1 = 24

if out == 1:
    DO = DO1  # green Light -> Open Gate
else:
    DO = DO0  # red Light -> AccessDenied

config = configparser.ConfigParser()
config.read('config.ini')

try:
    TimeOpen = int(config['GatOpen']['TimeOpen'])
except Exception as e:
    print("config parameter 'TimeOpen' wrong or missing")
    sys.exit(0)

GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
GPIO.setup(DO, GPIO.OUT)
GPIO.output(DO, 1)
sleep(TimeOpen)
GPIO.output(DO, 0)
