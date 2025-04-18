import configparser
from datetime import datetime, timedelta
from classes.mySQL import *
from classes.offlineBcTypeA import *

class portalumBcTypeA:
    def __init__(self, logger):
        self.active = False
        self.init = False
        self.canUse = False
        self.errMsg = ""
        self.logger = logger
        self.insertID = None
        self.access = None
        self.cursor = None
        self.commit = None

        self.db = mySQL(logger)
        if not self.db.init:
            print('portalumBcTypeA: mySQL Init failed!')
            if self.logger is not None:
                self.logger.info('portalumBcTypeA: mySQL Init failed!')
            self.errMsg = 'portalumBcTypeA: mySQL Init failed!'
            return

        self.cursor = self.db.cursor
        self.commit = self.db.commit
        self.getConfig()

        self.BC = offlineBcTypeA(logger)

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('datas/config.ini')
        try:
            self.active = self.str2bool(config['Modules']['PortalumBcTypeA'])
            self.maxEntrys = int(config['portalumBcTypeA']['maxEntrys'])
            self.timeLimit = int(config['portalumBcTypeA']['timeLimit'])
            self.timeCleanUp = int(config['portalumBcTypeA']['timeCleanUp'])
            self.init = True
            if self.init and self.init:
                self.canUse = True
        except Exception as error:
            print('config portalumBcTypeA parameter missing')
            if self.logger is not None:
                self.logger.info('config portalumBcTypeA parameter missing')
            self.errMsg = 'config portalumBcTypeA parameter missing'
            pass

        return

# --------------- Database Functions --------------- #
# Table: pbcta_entry

    def getDatabase(self):
        self.cursor.execute("select database()")
        return self.cursor.fetchone()[0]

    def checkAccess(self, access):
        pass

    def processBarcode(self, arrBC):
        if not arrBC['recognized']:
            if arrBC['BC'] != "":
                pass


        return arrBC
