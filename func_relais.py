#!/usr/bin/env python

import serial


def GetRS485() -> serial.Serial:
    s = serial.Serial("/dev/ttyACM0", 9600, timeout=0.5)
    s.flush
    return s


def ModbusCRC(msg: str) -> int:
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc


def RelaisOn(address: int, number: int) -> bytearray:
    s = GetRS485()

    cmd = [0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = address  # Device address
    cmd[1] = 0x05  # command
    cmd[2] = 0x00
    cmd[3] = number
    cmd[4] = 0xFF
    cmd[5] = 0x00
    crc = ModbusCRC(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    s.write(cmd)
    r = s.read(6)
    if (len(r) == 6):
        return r
    else:
        return {0x00}


def RelaisOff(address: int, number: int) -> bytearray:
    s = GetRS485()

    cmd = [0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = address  # Device address
    cmd[1] = 0x05  # command
    cmd[2] = 0x00
    cmd[3] = number
    cmd[4] = 0x00
    cmd[5] = 0x00
    crc = ModbusCRC(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    s.write(cmd)
    r = s.read(6)
    if (len(r) == 6):
        return r
    else:
        return {0x00}


def GetStatus(address: int, number: int) -> int:
    s = GetRS485()

    cmd = [0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = address  # Device address
    cmd[1] = 0x01  # command
    cmd[2] = 0x00
    cmd[3] = 0x00
    cmd[4] = 0x00
    cmd[5] = 0x08
    crc = ModbusCRC(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    s.write(cmd)
    r = s.read(6)
    if (len(r) == 6):
        if (number == 255):
            return r[3]
        else:
            if (r[3] & (1 << number)) != 0:
                return 1
            else:
                return 0
    else:
        return -1


def SetStatus(address: int, bit: str) -> bytearray:
    s = GetRS485()
    number = int(bit, 2)

    cmd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = address  # Device address
    cmd[1] = 0x0F  # command
    cmd[2] = 0x00
    cmd[3] = 0x00
    cmd[4] = 0x00
    cmd[5] = 0x08
    cmd[6] = 0x01
    cmd[7] = number
    crc = ModbusCRC(cmd[0:8])
    cmd[8] = crc & 0xFF
    cmd[9] = crc >> 8
    s.write(cmd)
    r = s.read(6)
    if (len(r) == 6):
        return r
    else:
        return {0x00}


def ReadAddr() -> bytearray:
    s = GetRS485()

    cmd = [0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = 0x00  # Device address
    cmd[1] = 0x03  # command
    cmd[2] = 0x40
    cmd[3] = 0x00
    cmd[4] = 0x00
    cmd[5] = 0x01
    crc = ModbusCRC(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    s.write(cmd)
    r = s.read(5)
    if (len(r) == 5):
        return {r[3], r[4]}
    else:
        return {0x00}


def ReadVersion() -> str:
    s = GetRS485()

    cmd = [0, 0, 0, 0, 0, 0, 0, 0]
    cmd[0] = 0x00  # Device address
    cmd[1] = 0x03  # command
    cmd[2] = 0x80
    cmd[3] = 0x00
    cmd[4] = 0x00
    cmd[5] = 0x01
    crc = ModbusCRC(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    s.write(cmd)
    r = s.read(5)
    if (len(r) == 5):
        return 'V{:.2f}'.format(int.from_bytes({r[3], r[4]}, byteorder='big', signed=False) / 100)
    else:
        return "-1"


def ByteArr2Hex(array: bytearray) -> str:
    return ' ' . join(format(i, '02x').upper() for i in array)
