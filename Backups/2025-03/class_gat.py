from func_main import *
import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep             # lets us have a delay

class Gat:
    def __init__(self):
        try:
            cfgGat = getGatConfig()
        except Exception as error:
            print(error.args)
            exit(0)

        self.TimeOpen = cfgGat[0]


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
        sleep(self.TimeOpen)
        GPIO.output(DO, 0)
