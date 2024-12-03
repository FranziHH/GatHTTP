#!/usr/bin/env python

import serial
import time
from functions import *

try:
    req_params = getConfigRequestParams()
except Exception as error:
    print(error.args)
    exit(0)

try:
    cfgRs232 = getConfigReader()

    baud_rate = cfgRs232[0]
    com_port = cfgRs232[1]
    bc_prefix = cfgRs232[2]
    rs232_timeout = cfgRs232[3]
    rfid_switch_pairs = cfgRs232[4]
    rfid_convert_to_dec = cfgRs232[5]
except Exception as error:
    print(error.args)
    exit(0)

ser = serial.Serial(com_port, baud_rate)
ser.flush

buffer = ""
barcode = ""
rfid = ""
while 1:
    if (ser.inWaiting() > 0):
        buffer += str(ser.read(ser.inWaiting()))

        # wait for new data after each line
        timeout = time.time() + rs232_timeout
        while not ser.inWaiting() and timeout > time.time():
            pass
        if not ser.inWaiting():
            # break
            tmp_bc = buffer[2:-1]
            if (tmp_bc[:len(bc_prefix)] == bc_prefix):
                # Barcode
                barcode = tmp_bc[len(bc_prefix):]
                print('BC:' + barcode)
            else:
                # RFID
                if (rfid_switch_pairs == 1):
                    count = len(tmp_bc)
                    rfidHex = ''
                    while count > 1:
                        rfidHex += tmp_bc[count - 2:count]
                        count -= 2
                else:
                    rfidHex = tmp_bc

                if (rfid_convert_to_dec == 1):
                    rfid = str(int(rfidHex, 16))
                else:
                    rfid = rfidHex

                print("RFID:" + rfid)

            print("-----")
            buffer = ""
            barcode = ""
            rfid = ""
