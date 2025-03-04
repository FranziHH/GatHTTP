#!/usr/bin/env python

from class_rs232 import *
import time

ser = RS232()

# ser.BeepWarning(3)

#WriteLED('green', 2000)
#time.sleep(2)
#WriteLED('red', 2000)
#time.sleep(2)

while(1):
    retBC = ser.ReadBarcode()
    if retBC[0] != "":
        print('BC: ' + retBC[0])
    else:
        print('RFID: ' + retBC[1])

    print("-----")
