#!/usr/bin/env python
import os
import signal
import sys
from classes.logger import *
from classes.rs232 import *
from classes.remoteAccess import *
from classes.mcDonalds import *
from classes.maintenance import *

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

# ----- Init remoteAccess ----- #
cRemoteAccess = remoteAccess(cLogger)
if not cRemoteAccess.canUse:
    print("RemoteAccess cannot be used -> Show Error on Log!")
    cLogger.info("RemoteAccess cannot be used -> Show Error on Log!")
    isremoteAccess = False
# ----- Init remoteAccess ----- #

# ----- Init mcDonalds ----- #
cMcDonalds = mcDonalds(cLogger)
if not cMcDonalds.canUse:
    print("McDonalds cannot be used -> Show Error on Log!")
    cLogger.info("McDonalds cannot be used -> Show Error on Log!")
    isMcDonalds = False
# ----- Init mcDonalds ----- #

# ----- Init Modules ----- #
cMaintenance = maintenance()
# ----- Init Modules ----- #

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
            # retBC['BC'] - Barcode
            # retBC['RFID'] - RFID
            if retBC['BC'] != "":
                print('BC: ' + retBC['BC'])
                cLogger.info('BC: ' + retBC['BC'])
            elif retBC['RFID'] != "":
                print('RFID: ' + retBC['RFID'])
                cLogger.info('RFID: ' + retBC['RFID'])
            else:
                print('retBC is empty')
                cLogger.info('retBC is empty')
                continue

            # process all modules - main (remoteAccess) last!
            retBC = cMcDonalds.processBarcode(retBC)
            retBC = cRemoteAccess.processBarcode(retBC)
            retBC = cMaintenance.processBarcode(retBC)
            # print(retBC)

            retGatOpen = cRs232.GatOpen(retBC['access'])
            retGatOpen['procModule'] = retBC['procModule']
            print(retGatOpen)

            # check, if access successfull
            cMcDonalds.checkAccess(retGatOpen)
            cRemoteAccess.checkAccess(retGatOpen)

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
