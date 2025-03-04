#!/usr/bin/env python

import serial
import time
from functions.func_main import *
from functions.func_rs232 import *

try:
    cfgRs232 = getConfigReader()
except Exception as error:
    print(error.args)
    exit(0)

baud_rate = cfgRs232[0]
com_port = cfgRs232[1]
bc_prefix = cfgRs232[2]
rs232_timeout = cfgRs232[3]

ser = serial.Serial(com_port, baud_rate)
ser.flush

BeepWarning(ser, 3)
time.sleep(.5)
BeepEntry(ser, 3)
time.sleep(.5)
BeepFailed(ser, 3)
