#!/usr/bin/env python

from classes.rs232 import *

ser = RS232()

while (1):
    retBC = ser.ReadBarcode()
    # retBC[0] - Barcode
    # retBC[1] - RFID
    if retBC[0] != "":
        print('BC: ' + retBC[0])
    else:
        print('RFID: ' + retBC[1])
