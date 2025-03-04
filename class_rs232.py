from func_main import *
import RPi.GPIO as GPIO            # import RPi.GPIO module
import serial
import time

class RS232:
    def __init__(self):
        try:
            cfgRs232 = getConfigReader()
            cfgGat = getGatConfig()
        except Exception as error:
            print(error.args)
            exit(0)

        self.baud_rate = cfgRs232[0]
        self.com_port = cfgRs232[1]
        self.bc_prefix = cfgRs232[2]
        self.rs232_timeout = cfgRs232[3]
        self.switch_pairs = cfgRs232[4]
        self.convert_to_dec = cfgRs232[5]

        self.TimeOpen = cfgGat[0]
        self.WarnLoop = cfgGat[1]

        self.serial = serial.Serial(self.com_port, self.baud_rate)
        self.serial.flush

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

        return

    def ReadBarcode(self):
        buffer = ""
        barcode = ""
        rfid = ""
        loopFlag = True

        # first flush all datas
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

        if out == "1":
            self.BeepEntry(self.WarnLoop)
        else:
            self.BeepWarning(self.WarnLoop)

        time.sleep(self.TimeOpen)
        GPIO.output(DO, 0)

        return