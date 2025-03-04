#!/usr/bin/env python

from class_rs232 import *
from class_request import *
from class_gat import *

req = Request()
ser = RS232()

while(1):
    retBC = {}
    retBC = ser.ReadBarcode()
    if retBC[0] != "":
        print('BC: ' + retBC[0])
    else:
        print('RFID: ' + retBC[1])

    req.JsonRequest("TestDevice Mit ÄÖÜ", retBC[0], retBC[1])
    print(req.retStr)
    print(req.access)
    ser.GatOpen(req.access)
    ser.serial.flush
    print("-----")
