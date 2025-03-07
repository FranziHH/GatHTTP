#!/usr/bin/env python

from classes.rs232 import *

ser = RS232()

ser.serial.write(ser.SetBeep(2000, 200, 20))
time.sleep(.25)
ser.serial.write(ser.SetBeep(1000, 500, 20))
time.sleep(.35)