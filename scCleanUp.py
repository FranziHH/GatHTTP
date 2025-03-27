#!/usr/bin/env python
import os
import sys
# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

import logging
from pathlib import Path
from datetime import datetime
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/' + datetime.today().strftime('%Y-%m-%d') + '_' + Path(__file__).stem + '.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    encoding='utf-8',
                    level=logging.DEBUG)

logger.info("-----")
logger.info('Start')
logger.info("-----")

from classes.scMySQL import *

myDB = scMySQL(logger)

if not myDB.active:
    print("scReader isn't activated!")
    logger.info("scReader isn't activated!")
    exit()

myDB.cleanUP()
