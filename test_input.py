#!/usr/bin/env python
import os
import signal
import sys

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

def main():
    msg = ''
    lastMsg = ''
    try:
        while True:
            if GPIO.input(DI0):
                GPIO.output(DO0, 1)
                msg = "DI0 - ON , "
            else:
                GPIO.output(DO0, 0)
                msg = "DI0 - OFF, "

            if GPIO.input(DI1):
                GPIO.output(DO1, 1)
                msg += "DI1 - ON "
            else:
                GPIO.output(DO1, 0)
                msg += "DI1 - OFF"

            if msg != lastMsg:
                lastMsg = msg
                print(msg)

            sleep(0.1)

    except Exception as error:
        print('Error: ' + error.args)
        pass
        

def signal_handler(sig, frame):
    GPIO.cleanup()
    print("Stopping...")
    sys.exit(0)


# Setze den Signal-Handler für SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Deaktiviere die Terminal-Ausgabe für Zeichen wie ^C
os.system('stty -echoctl')

if __name__ == "__main__":
    main()