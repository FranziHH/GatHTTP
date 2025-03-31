#!/usr/bin/env python
import os
import sys
# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

import logging
from pathlib import Path
from datetime import datetime
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/' + datetime.today().strftime('%Y-%m-%d') + '_' + Path(__file__).stem + '.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    encoding='utf-8',
                    level=logging.DEBUG)

logger.info("-----")
logger.info('Start')
logger.info("-----")

from classes.rs232 import *
from classes.request import *
from classes.scReader import *
from classes.scMySQL import *

req = Request(logger)
ser = RS232(logger)
reader = scReader()
myDB = scMySQL(logger)

logger.info('classes created')
logger.info("-----")
ser.BeepOhNo(1)

if not req.active:
    print('Request is not active!')
    print("-----")
    logger.info('Request is not active!')
    logger.info("-----")

def doServiceCode(barcode):
    barcode_data = reader.decode_barcode(barcode)
    retData = myDB.processBarcode(barcode_data)
    ser.GatOpen(str(retData['entry']))
    return

try:
    while (True):
        retBC = ser.ReadBarcode()
        # retBC[0] - Barcode
        # retBC[1] - RFID
        if retBC[0] != "":
            print('BC: ' + retBC[0])
            logger.info('BC: ' + retBC[0])

            if myDB.active:
                if reader.isValid(retBC[0]):
                    print('exec ServiceCode')
                    logger.info('exec ServiceCode')
                    doServiceCode(retBC[0])
                    continue

        else:
            print('RFID: ' + retBC[1])
            logger.info('RFID: ' + retBC[1])

        if req.active:
            retReq = req.JsonRequest(ser.GatName, retBC[0], retBC[1])
            # retReq[0] - Status (True/False)
            # retReq[1] - Return Message (Text)
            # retReq[2] - Access 0 - False, 1 - True (String)
            if (retReq[0]):
                print(retReq[1])
                logger.info(retReq[1].replace("\n", ", "))
                ser.GatOpen(retReq[2])
            else:
                print('Error: ' + retReq[1].replace("\n", ", "))
                logger.error(retReq[1])

        print("-----")
        logger.info("-----")

except Exception as error:
    print('Error: ' + error.args)
    logger.error('Error: ' + error.args)
    pass

except KeyboardInterrupt as error:
    print("Stopping...")
    logger.info("Stopping...")
