#!/usr/bin/env python
import os

from classes.logger import *
cLogger = logger(os.path.basename(__file__)).logger

cLogger.info("-----")
cLogger.info('Start')
cLogger.info("-----")

from classes.mcDonalds import *

cMcDonalds = mcDonalds(cLogger)

if not cMcDonalds.active:
    print("McDonalds isn't activated!")
    cLogger.info("McDonalds isn't activated!")
    exit()

if not cMcDonalds.init:
    print("McDonalds Settings failed!")
    cLogger.info("McDonalds Settings failed!")
    exit()

cMcDonalds.cleanUP()
