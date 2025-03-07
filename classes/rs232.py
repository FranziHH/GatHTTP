import RPi.GPIO as GPIO            # import RPi.GPIO module
import serial
import time
import configparser


class RS232:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('datas/config.ini')

        try:
            self.getConfigReader()
            self.getGatConfig()
        except Exception as error:
            print(error.args)
            exit(0)

        self.serial = serial.Serial(self.com_port, self.baud_rate)
        self.serial.flush
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def getConfigReader(self):
        try:
            self.baud_rate = self.config['Reader']['baud_rate']
            self.com_port = self.config['Reader']['com_port']
            self.bc_prefix = self.config['Reader']['bc_prefix']
            self.rs232_timeout = float(self.config['Reader']['timeout'])
            self.switch_pairs = int(self.config['Reader']['rfid_switch_pairs'])
            self.convert_to_dec = int(self.config['Reader']['rfid_convert_to_dec'])
        except Exception as error:
            raise RuntimeError('config Reader parameter missing') from error

        return

    def getGatConfig(self):
        try:
            self.TimeOpen = int(self.config['GatOpen']['TimeOpen'])
            self.WarnLoop0 = int(self.config['GatOpen']['WarnLoop0'])
            self.WarnLoop1 = int(self.config['GatOpen']['WarnLoop1'])
            self.UseBeep = self.str2bool(self.config['GatOpen']['UseBeep'])
            self.GatName = self.config['GatOpen']['GatName']
        except Exception as error:
            raise RuntimeError('getGatConfig parameter missing') from error

        return

    # color: GREEN/RED
    # time: max 4 digits as MilliSeconds '1000' = 1 Second
    def SetLED(self, color: str, time: int):
        time = str(time)
        if (len(time) > 4):
            time = time[0:4]
        time = time.zfill(4)

        color = color.upper()
        LED = '\x7E\x010000#LEDONSXCXXXXD;\x03'
        if (color == 'GREEN'):
            LED = LED.replace("XC", "2C")
        else:
            LED = LED.replace("XC", "0C")

        LED = LED.replace("XXXXD", time + "D")

        return LED.encode()

    # freq: max 4 digits as Hertz '1000' = 1000Hz
    # time: max 3 digits as MilliSeconds '100' = 0.1 Second
    # vol: max 2 digits as volume 1 - 20: Loudest 20

    def SetBeep(self, freq: int, time: int, vol: int):
        freq = str(freq)
        if (len(freq) > 4):
            freq = freq[0:4]
        freq = freq.zfill(4)

        time = str(time)
        if (len(time) > 3):
            time = time[0:3]
        time = time.zfill(3)

        vol = str(vol)
        if (len(vol) > 3):
            vol = vol[0:3]
        vol = vol.zfill(3)

        BEEP = '\x7E\x010000#BEEPONXXXXFXXXTXXV;\x03'
        BEEP = BEEP.replace("XXXXF", freq + "F")
        BEEP = BEEP.replace("XXXT", time + "T")
        BEEP = BEEP.replace("XXV", vol + "V")
        return BEEP.encode()

    def WriteLED(self, color: str, time: int):
        self.serial.write(self.SetLED(color, time))
        return

    def BeepWarning(self, repeat: int):
        j = 0
        while (j < repeat):
            j += 1
            self.serial.write(self.SetLED("red", 1200))

            i = 0
            while (i < 3):
                i += 1
                self.serial.write(self.SetBeep(2000, 200, 20))
                time.sleep(.2)
                self.serial.write(self.SetBeep(1000, 200, 20))
                time.sleep(.2)

        time.sleep(.2)
        return

    def BeepOhNo(self, repeat: int):
        j = 0
        while (j < repeat):
            j += 1
            self.serial.write(self.SetLED("red", 1200))

            self.serial.write(self.SetBeep(2000, 200, 20))
            time.sleep(.25)
            self.serial.write(self.SetBeep(1000, 500, 20))
            time.sleep(.35)

        time.sleep(.2)
        return


    def BeepFailed(self, repeat: int):
        j = 0
        while (j < repeat):
            j += 1
            self.serial.write(self.SetLED("red", 1200))
            time.sleep(.1)

            freq = 2000
            while (freq > 300):
                freq -= 100
                self.serial.write(self.SetBeep(freq, 50, 20))
                time.sleep(.05)

        time.sleep(.2)
        return

    def BeepEntry(self, repeat: int):
        j = 0
        while (j < repeat):
            j += 1
            self.serial.write(self.SetLED("green", 1200))
            time.sleep(.1)

            freq = 500
            while (freq < 2300):
                freq += 100
                self.serial.write(self.SetBeep(freq, 50, 20))
                time.sleep(.05)

        time.sleep(.2)
        return

    def ReadBarcode(self):
        # retBC[0] - Barcode
        # retBC[1] - RFID
        buffer = ""
        barcode = ""
        rfid = ""
        loopFlag = True

        self.serial.flush
        # flush does not do what you expect, workaround is read_all
        self.serial.read_all()

        while loopFlag:
            if (self.serial.inWaiting() > 0):
                buffer += str(self.serial.read(self.serial.inWaiting()))

                # wait for new data after each line
                timeout = time.time() + self.rs232_timeout
                while not self.serial.inWaiting() and timeout > time.time():
                    pass
                if not self.serial.inWaiting():
                    # break
                    tmp_bc = buffer[2:-1]
                    if (tmp_bc[:len(self.bc_prefix)] == self.bc_prefix):
                        # Barcode
                        barcode = tmp_bc[len(self.bc_prefix):]
                        loopFlag = False
                    else:
                        # RFID
                        if (self.switch_pairs == 1):
                            count = len(tmp_bc)
                            rfidHex = ''
                            while count > 1:
                                rfidHex += tmp_bc[count - 2:count]
                                count -= 2
                        else:
                            rfidHex = tmp_bc

                        if (self.convert_to_dec == 1):
                            rfid = str(int(rfidHex, 16))
                        else:
                            rfid = rfidHex

                        loopFlag = False

        return barcode, rfid

    def GatOpen(self, out: str):
        # Set Output GPIOs
        DO0 = 23
        DO1 = 24

        if out == "1":
            DO = DO1  # green Light -> Open Gate
        else:
            DO = DO0  # red Light -> AccessDenied

        GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
        GPIO.setup(DO, GPIO.OUT)
        GPIO.output(DO, 1)

        if self.UseBeep:
            if out == "1":
                self.BeepEntry(self.WarnLoop0)
            else:
                # self.BeepWarning(self.WarnLoop)
                self.BeepOhNo(self.WarnLoop1)

        time.sleep(self.TimeOpen)
        GPIO.output(DO, 0)

        return
