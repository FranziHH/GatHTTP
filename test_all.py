#!/usr/bin/env python
import os
import sys
# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

from classes.rs232 import *
from classes.request import *

req = Request()
ser = RS232()

while (1):
    retBC = ser.ReadBarcode()
    # retBC[0] - Barcode
    # retBC[1] - RFID
    if retBC[0] != "":
        print('BC: ' + retBC[0])
    else:
        print('RFID: ' + retBC[1])

    retReq = req.JsonRequest(ser.GatName, retBC[0], retBC[1])
    # retReq[0] - Status (True/False)
    # retReq[1] - Return Message (Text)
    # retReq[2] - Access 0 - False, 1 - True (String)
    print(retReq[1])
    ser.GatOpen(retReq[2])
    print("-----")
