import time

# color: GREEN/RED
# time: max 4 digits as MilliSeconds '1000' = 1 Second


def SetLED(color: str, time: int):
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


def SetBeep(freq: int, time: int, vol: int):
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


def BeepWarning(ser: object, repeat: int):
    j = 0
    while (j < repeat):
        j += 1
        ser.write(SetLED("red", 1200))

        i = 0
        while (i < 3):
            i += 1
            ser.write(SetBeep(2000, 200, 20))
            time.sleep(.2)
            ser.write(SetBeep(1000, 200, 20))
            time.sleep(.2)

    return


def BeepFailed(ser: object, repeat: int):
    j = 0
    while (j < repeat):
        j += 1
        ser.write(SetLED("red", 1200))
        time.sleep(.1)

        freq = 2000
        while (freq > 300):
            freq -= 100
            ser.write(SetBeep(freq, 50, 20))
            time.sleep(.05)

    return


def BeepEntry(ser: object, repeat: int):
    j = 0
    while (j < repeat):
        j += 1
        ser.write(SetLED("green", 1200))
        time.sleep(.1)

        freq = 500
        while (freq < 2300):
            freq += 100
            ser.write(SetBeep(freq, 50, 20))
            time.sleep(.05)

    return
