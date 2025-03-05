#!/usr/bin/env python

import serial


class RS485:
    def __init__(self):
        self.serial = serial.Serial("/dev/ttyACM0", 9600, timeout=0.5)
        self.serial.flush
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def ModbusCRC(self, msg: str) -> int:
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

    def RelaisOn(self, address: int, number: int) -> int:
        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        cmd[0] = address  # Device address
        cmd[1] = 0x05  # command
        cmd[2] = 0x00
        cmd[3] = number
        cmd[4] = 0xFF
        cmd[5] = 0x00
        crc = self.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        self.serial.write(cmd)
        r = self.serial.read(6)
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        if (bytes(cmd[0:6]) == r):
            return 1
        else:
            return -1

    def RelaisOff(self, address: int, number: int) -> int:
        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        cmd[0] = address  # Device address
        cmd[1] = 0x05  # command
        cmd[2] = 0x00
        cmd[3] = number
        cmd[4] = 0x00
        cmd[5] = 0x00
        crc = self.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        self.serial.write(cmd)
        r = self.serial.read(6)
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        if (bytes(cmd[0:6]) == r):
            return 1
        else:
            return -1

    def GetStatus(self, address: int, number: int) -> str:
        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        cmd[0] = address  # Device address
        cmd[1] = 0x01  # command
        cmd[2] = 0x00
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = 0x08
        crc = self.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        self.serial.write(cmd)
        r = self.serial.read(6)
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        if (len(r) == 6):
            if (number == 255):
                return "{:0>8b}".format(r[3])
            else:
                if (r[3] & (1 << number)) != 0:
                    return "1"
                else:
                    return "0"
        else:
            return "-1"

    def SetStatus(self, address: int, bit: str) -> int:
        # Bit: must be 8 Bits
        if (len(bit) == 8):
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
            crc = self.ModbusCRC(cmd[0:8])
            cmd[8] = crc & 0xFF
            cmd[9] = crc >> 8
            # flush does not do what you expect, workaround is read_all
            self.serial.read_all()
            self.serial.write(cmd)
            r = self.serial.read(6)
            # flush does not do what you expect, workaround is read_all
            self.serial.read_all()
            if (bytes(cmd[0:6]) == r):
                return 1
            else:
                return -1
        else:
            return -2

    def GetAddr(self) -> int:
        # connect only ONE device
        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        cmd[0] = 0x00  # Device address
        cmd[1] = 0x03  # command
        cmd[2] = 0x40
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = 0x01
        crc = self.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        self.serial.write(cmd)
        r = self.serial.read(5)
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        if (len(r) == 5):
            return r[4]
        else:
            return -1

    def SetAddr(self, address: int) -> int:
        # connect only ONE device
        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        cmd[0] = 0x00  # Device address
        cmd[1] = 0x06  # command
        cmd[2] = 0x40
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = address
        crc = self.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        self.serial.write(cmd)
        r = self.serial.read(6)
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        if (len(r) == 6):
            return r[5]
        else:
            return -1

    def GetVersion(self, address: int) -> str:
        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        cmd[0] = address  # Device address
        cmd[1] = 0x03  # command
        cmd[2] = 0x80
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = 0x01
        crc = self.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        self.serial.write(cmd)
        r = self.serial.read(5)
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        if (len(r) == 5):
            return 'V{:.2f}'.format(int.from_bytes([r[3], r[4]], byteorder='big', signed=False) / 100)
        else:
            return "-1"

    def SetBaudRate(self, address: int, baud: int) -> int:
        # 0: 4800
        # 1: 9600
        # 2: 19200
        # 3: 38400
        # 4: 57600
        # 5: 115200
        # 6: 128000
        # 7: 256000

        cmd = [0, 0, 0, 0, 0, 0, 0, 0]
        cmd[0] = address  # Device address
        cmd[1] = 0x06  # command
        cmd[2] = 0x20
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = baud
        crc = self.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        self.serial.write(cmd)
        r = self.serial.read(6)
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()
        if (bytes(cmd[0:6]) == r):
            return 1
        else:
            return -1

    def ByteArr2Hex(self, array: bytearray) -> str:
        return ' ' . join(format(i, '02x').upper() for i in array)
