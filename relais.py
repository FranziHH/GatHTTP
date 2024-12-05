#!/usr/bin/env python

# if you gets error like "usr/bin/env: ‘python\r’: No such file or directory"
# convert file from dos into unix: "dos2unix [filename]"

from func_rs485 import *
import time

# print(RelaisOn(1, 7))
# print(RelaisOff(1, 255))

# print(SetStatus(1, '10101010'))
# print(SetStatus(2, '01010101'))

print(GetStatus(1, 255))
print(GetStatus(2, 255))

# print(SetAddr(2))
# print(GetAddr())

# print(GetVersion(1))

# 0: 4800
# 1: 9600
# 2: 19200
# 3: 38400
# 4: 57600
# 5: 115200
# 6: 128000
# 7: 256000
# print(SetBaudRate(1))
