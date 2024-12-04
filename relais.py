#!/usr/bin/env python

# if you gets error like "usr/bin/env: ‘python\r’: No such file or directory"
# convert file from dos into unix: "dos2unix [filename]"

from func_relais import *
import time

# RelaisOn(1, 4)
# print(ByteArr2Hex(RelaisOn(1, 0)))

# setStatus(1, '01010101')
print(ByteArr2Hex(RelaisOff(1, 255)))
time.sleep(0.5)


print(getStatus(1, 255))
# print(hex(getStatus(1, 4)))

# print(ByteArr2Hex(ReadAddr()))

# print(ReadVersion())