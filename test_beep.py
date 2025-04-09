#!/usr/bin/env python

from classes.rs232 import *

cRs232 = rs232(None)

cRs232.serial.write(cRs232.SetBeep(2000, 200, 20))
time.sleep(.25)
cRs232.serial.write(cRs232.SetBeep(1000, 500, 20))
time.sleep(.35)
