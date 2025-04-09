#!/usr/bin/env python
import os
import signal
import sys
from classes.logger import *
from classes.rs232 import *
from classes.gatHttp import *
from classes.mcDonalds import *

# ----- Init Logger ----- #
cLogger = logger(os.path.basename(__file__)).logger

cLogger.info("-----")
cLogger.info('Start')
cLogger.info("-----")
# ----- Init Logger ----- #

# ----- Init rs232 ----- #
cRs232 = rs232(cLogger)
if not cRs232.init:
    print("rs232 Settings failed!")
    cLogger.info("rs232 Settings failed!")
    exit()
# ----- Init rs232 ----- #

# ----- Init gatHttp ----- #
isGatHTTP = True
cGatHttp = gatHttp(cLogger)

if not cGatHttp.active:
    print("gatHttp isn't activated!")
    cLogger.info("gatHttp isn't activated!")
    isGatHTTP = False

if not cGatHttp.init:
    print("gatHttp Settings failed!")
    cLogger.info("gatHttp Settings failed!")
    isGatHTTP = False
# ----- Init gatHttp ----- #

# ----- Init mcDonalds ----- #
isMcDonalds = True
cMcDonalds = mcDonalds(cLogger)

if not cMcDonalds.active:
    print("McDonalds isn't activated!")
    cLogger.info("McDonalds isn't activated!")
    isMcDonalds = False

if not cMcDonalds.init:
    print("McDonalds Settings failed!")
    cLogger.info("McDonalds Settings failed!")
    isMcDonalds = False
# ----- Init mcDonalds ----- #

# ----- Init Modules [n] ----- #
# ....... and so on
# ----- Init Modules [n] ----- #

cLogger.info('classes created')
cLogger.info("-----")
cRs232.BeepOhNo(1)

def main():
    try:
        while (True):
            retBC = cRs232.ReadBarcode()
            print(retBC)
            
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
