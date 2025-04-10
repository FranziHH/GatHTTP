#!/usr/bin/env python
from classes.mcDonalds import *
from classes.remoteAccess import *
from classes.rs232 import *
import os
import signal
import sys

from classes.logger import *
cLogger = logger(os.path.basename(__file__)).logger

cLogger.info("-----")
cLogger.info('Start')
cLogger.info("-----")


cRemoteAccess = remoteAccess(cLogger)
cRS232 = rs232(cLogger)
cMcDonalds = mcDonalds(cLogger)

cLogger.info('classes created')
cLogger.info("-----")
cRS232.BeepOhNo(1)

if not cRemoteAccess.init:
    print('remoteAccess is not init!')
    print("-----")
    cLogger.info('remoteAccess is not init!')
    cLogger.info("-----")


def doMcDonalds(barcode):
    barcode_data = cMcDonalds.decode_barcode(barcode)
    retData = cMcDonalds.processBarcode(barcode_data)
    cRS232.GatOpen(str(retData['entry']))
    return


def doremoteAccess(retBC):
    request = cRemoteAccess.JsonRequest(cRemoteAccess.GatName, retBC['BC'], retBC['RFID'])
    # request[0] - Status (True/False)
    # request[1] - Return Message (Text)
    # request[2] - Access 0 - False, 1 - True (String)
    if (request[0]):
        print(request[1])
        cLogger.info(request[1].replace("\n", ", "))
        cRS232.GatOpen(request[2])
    else:
        print('Error: ' + request[1].replace("\n", ", "))
        cLogger.error(request[1])
    return


def main():
    try:
        while (True):
            retBC = cRS232.ReadBarcode()
            # retBC['BC'] - Barcode
            # retBC['RFID'] - RFID
            if retBC['BC'] != "":
                print('BC: ' + retBC['BC'])
                cLogger.info('BC: ' + retBC['BC'])

                if cMcDonalds.init:
                    if cMcDonalds.isValid(retBC['BC']):
                        print('exec McDonalds')
                        cLogger.info('exec McDonalds')
                        doMcDonalds(retBC['BC'])
                        print("-----")
                        cLogger.info("-----")
                        continue

            else:
                print('RFID: ' + retBC['RFID'])
                cLogger.info('RFID: ' + retBC['RFID'])

            if cRemoteAccess.init:
                print('exec remoteAccess')
                cLogger.info('exec remoteAccess')
                doremoteAccess(retBC)
                print("-----")
                cLogger.info("-----")
                continue

            print("-----")
            cLogger.info("-----")

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
