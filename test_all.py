#!/usr/bin/env python
from classes.mcDonalds import *
from classes.gatHttp import *
from classes.rs232 import *
import os
import signal
import sys

from classes.logger import *
cLogger = logger(os.path.basename(__file__)).logger

cLogger.info("-----")
cLogger.info('Start')
cLogger.info("-----")


cGatHttp = gatHttp(cLogger)
cRS232 = rs232(cLogger)
cMcDonalds = mcDonalds(cLogger)

cLogger.info('classes created')
cLogger.info("-----")
cRS232.BeepOhNo(1)

if not cGatHttp.init:
    print('GatHttp is not init!')
    print("-----")
    cLogger.info('GatHttp is not init!')
    cLogger.info("-----")


def doMcDonalds(barcode):
    barcode_data = cMcDonalds.decode_barcode(barcode)
    retData = cMcDonalds.processBarcode(barcode_data)
    cRS232.GatOpen(str(retData['entry']))
    return


def doGatHttp(retBC):
    request = cGatHttp.JsonRequest(cGatHttp.GatName, retBC[0], retBC[1])
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
            # retBC[0] - Barcode
            # retBC[1] - RFID
            if retBC[0] != "":
                print('BC: ' + retBC[0])
                cLogger.info('BC: ' + retBC[0])

                if cMcDonalds.init:
                    if cMcDonalds.isValid(retBC[0]):
                        print('exec McDonalds')
                        cLogger.info('exec McDonalds')
                        doMcDonalds(retBC[0])
                        print("-----")
                        cLogger.info("-----")
                        continue

            else:
                print('RFID: ' + retBC[1])
                cLogger.info('RFID: ' + retBC[1])

            if cGatHttp.init:
                print('exec GatHttp')
                cLogger.info('exec GatHttp')
                doGatHttp(retBC)
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
