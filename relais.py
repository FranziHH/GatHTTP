#!/usr/bin/env python

# if you gets error like "usr/bin/env: ‘python\r’: No such file or directory"
# convert file from dos into unix: "dos2unix [filename]"

from func_relais import *
import time

print(RelaisOn(1, 7))

# print(RelaisOff(1, 7))

# print(SetStatus(1, '01010101'))

# print(getStatus(1, 255))
# print(hex(getStatus(1, 4)))

# print(ByteArr2Hex(WriteAddr([0x00, 0x02])))
# print(WriteAddr([0x00, 0x01]))

# print(ByteArr2Hex({0x00, 0x02}))
# print(ReadVersion())

# print(ReadAddr())