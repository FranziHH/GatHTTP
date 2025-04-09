import os
import sys

# insert root directory into python module search path
sys.path.insert(1, os.getcwd())

import logging
from pathlib import Path
from datetime import datetime

class logger:
    def __init__(self, logname):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs/' + datetime.today().strftime('%Y-%m-%d') + '_' + Path(logname).stem + '.log',
                            format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            encoding='utf-8',
                            level=logging.DEBUG)
