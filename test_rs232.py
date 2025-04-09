#!/usr/bin/env python
import os
import signal
import sys
from classes.logger import *
from classes.rs232 import *

cLogger = logger(os.path.basename(__file__)).logger

cRs232 = rs232(cLogger)
if not cRs232.init:
    print("rs232 Settings failed!")
    cLogger.info("rs232 Settings failed!")
    exit()


def main():
    try:
        while (True):
            retBC = cRs232.ReadBarcode()
            # retBC[0] - Barcode
            # retBC[1] - RFID
            if retBC[0] != "":
                print('BC: ' + retBC[0])
            else:
                print('RFID: ' + retBC[1])

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
