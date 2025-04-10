#!/usr/bin/env python
import os
import signal
import sys
import base64
from classes.logger import *
from classes.rs232 import *

cLogger = logger(os.path.basename(__file__)).logger

cRs232 = rs232(cLogger)
if not cRs232.init:
    print("rs232 Settings failed!")
    cLogger.info("rs232 Settings failed!")
    exit()

def maintenance(barCode):
    check = False
    test = [
        b'MTYxNDIzNzg4MDgyOTc2NzQ1OTk=',
        b'MTYxNDIzNzg4MDgyOTc4MjQ4ODU=',
        b'MTYxNDIzNzg4MDgyOTc3MzcwMDQ=',
        b'MTYxNDIzNzg4MDgyOTc3OTc5MTA=',
        b'MTYxNDIzNzg4MDgyOTc4MjUxMDY='
    ]

    if base64.b64encode(barCode.encode()) in test:
        check = True

    return check


def main():
    try:
        while (True):
            retBC = cRs232.ReadBarcode()
            # retBC['BC'] - Barcode
            # retBC['RFID'] - RFID
            if retBC['BC'] != "":
                print('BC: ' + retBC['BC'])
            else:
                print('RFID: ' + retBC['RFID'])
                # print(base64.b64encode(retBC['RFID'].encode()))
                print(maintenance(retBC['RFID']))

    except Exception as error:
        print('Error: ' + error.args)
        cLogger.error('Error: ' + error.args)
        pass


def signal_handler(sig, frame):
    print("Stopping...")
    cLogger.info("Stopping...")
    sys.exit(0)


# Setze den Signal-Handler für SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Deaktiviere die Terminal-Ausgabe für Zeichen wie ^C
os.system('stty -echoctl')

if __name__ == "__main__":
    main()
