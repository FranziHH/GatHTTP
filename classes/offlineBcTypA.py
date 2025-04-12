import configparser
from datetime import datetime, timedelta
from classes.mySQL import *

class offlineBcTypA:
    def __init__(self, logger):
        self.active = False
        self.init = False
        self.canUse = False
        self.errMsg = ""
        self.logger = logger

        self.db = mySQL(logger)
        if not self.db.init:
            print('offlineBcTypA: mySQL Init failed!')
            if self.logger is not None:
                self.logger.info('offlineBcTypA: mySQL Init failed!')
            self.errMsg = 'offlineBcTypA: mySQL Init failed!'
            return

        self.cursor = self.db.cursor
        self.getConfig()

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('datas/config.ini')
        try:
            self.active = self.str2bool(config['Modules']['offlineBcTypA'])
            self.storeID = int(config['offlineBcTypA']['storeID'])
            self.maxEntrys = int(config['offlineBcTypA']['maxEntrys'])
            self.timeLimit = int(config['offlineBcTypA']['timeLimit'])
            self.timeCleanUp = int(config['offlineBcTypA']['timeCleanUp'])
            self.init = True
            if self.init and self.init:
                self.canUse = True
        except Exception as error:
            print('config offlineBcTypA parameter missing')
            if self.logger is not None:
                self.logger.info('config offlineBcTypA parameter missing')
            self.errMsg = 'config offlineBcTypA parameter missing'
            pass

        return

# --------------- Database Functions --------------- #

    def getDatabase(self):
        self.cursor.execute("select database()")
        return self.cursor.fetchone()[0]
    
    def processBarcode(self, arrBC):
        if self.canUse == False or arrBC['recognized'] or arrBC['BC'] == '':
            return arrBC

        if not self.isValid(arrBC['BC']):
            return arrBC

        arrBC['procModule'] = self.__class__.__name__
        arrBC['recognized'] = True
        arrBC['access'] = False

        datas = self.decode_barcode(arrBC['BC'])

        entry = None
        info = None

        if self.storeID != datas['storeID']:
            entry = 0
            info = "Access denied: wrong StoreID [barcodeStoreID: " + str(datas['storeID']) + ", localeStoreID: " + str(self.storeID) + "]"
        else:
            now = datetime.now()
            timeDiff = divmod((now - datas['dateTime']).total_seconds(), 60)[0] 
            if timeDiff > self.timeLimit:
                entry = 0
                info = "Access denied: time limit exceeded [barcodeTime: " + datas['strDateTime'] + ", accessTime: " + now.strftime('%Y-%m-%d %H:%M:%S') + ", Limit: " + str(self.timeLimit) + " minutes]"
            else:
                accessCount = self.countEntrys(datas['barcode'])
                if accessCount >= self.maxEntrys:
                    entry = 0
                    info = "Access denied: maximum number of accesses exceeded [usedEntrys: " + str(accessCount  ) + ", maxEntrys: " + str(self.maxEntrys) + "]"
                else:
                    entry = 1
                    info = "Access guaranteed"

        # insert Data into DB
        datas['entry'] = entry
        datas['info'] = info
        insertID = self.insertData(datas)

        retData = {'entry': entry, 'info': info, 'insertID': insertID}
        print("----- " + self.__class__.__name__ + ": processBarcode -----")
        print(retData)
        print("-----")
        if self.logger is not None:
            self.logger.info("----- " + self.__class__.__name__ + ": processBarcode -----")
            self.logger.info(retData)
            self.logger.info("-----")

        arrBC['access'] = bool(entry)
        arrBC['message'] = info

        return arrBC

    def insertData(self, datas):
        sql = "INSERT INTO mcd_entry (created_ts, store_id, pos_id, barcode, entry, info) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (datas['strDateTime'], datas['storeID'], datas['posID'], datas['barcode'], datas['entry'], datas['info'])
        self.cursor.execute(sql, val)
        self.db.commit
        return self.cursor.lastrowid
    
    def updateEntry(self, id, entry, info):
        sql = "UPDATE mcd_entry SET entry = %s, info = %s WHERE id = %s"
        val = (entry, info, id)
        self.cursor.execute(sql, val)
        self.db.commit
        return self.cursor.rowcount

    def countEntrys(self, bc):
        sql = "SELECT COUNT(id) FROM mcd_entry WHERE barcode = %s AND entry = 1"
        val = (bc, )
        self.cursor.execute(sql, val)
        return self.cursor.fetchone()[0]
    
    def cleanUP(self):
        tsCleanUP = datetime.now() - timedelta(days=self.timeCleanUp)
        stime = tsCleanUP.strftime('%Y-%m-%d %H:%M:%S')
        sql = "DELETE FROM mcd_entry WHERE current_ts < %s"
        val = (stime, )
        self.cursor.execute(sql, val)
        self.db.commit
        retVal = self.cursor.rowcount

        print("----- cleanUP -----")
        print('delete records before ' + stime)
        print(str(retVal) + ' records deleted')
        print("----- cleanUP -----")
        if self.logger is not None:
            self.logger.info("----- cleanUP -----")
            self.logger.info('delete records before ' + stime)
            self.logger.info(str(retVal) + ' records deleted')
            self.logger.info("----- cleanUP -----")

        return retVal
# --------------- Database Functions --------------- #

# --------------- class Functions --------------- #
# definition offline Barcode Type A
# https://portalum.atlassian.net/wiki/spaces/C/pages/684490753/TYP+A+Offline+Barcodes

    def decode_barcode(self, barcode):
        valid = False
        area = None             # 3 digits
        validUntil = None       # 4 digits
        tsValidUntil = None     # DateTime
        ticketNumber = None     # 4 digits
        ownIdentity = None      # 2 digits
        currentNumber = None    # 5 digits
        checkSum = None         # 2 digits
        
        if len(barcode) >= 18:
            area = barcode[0:3]
            validUntil = barcode[3:7]
            tsValidUntil = datetime(2009, 1, 1) + timedelta(days=int(validUntil)) - timedelta(seconds=1)
            ticketNumber = barcode[7:11]
            ownIdentity = barcode[11:13]
            currentNumber = barcode[13:18]
            if len(barcode) == 18:
                valid = True
            elif len(barcode) == 20:
                checkSum = barcode[18:20]

        return {
            'valid': valid,
            'area': area,
            'validUntil': validUntil,
            'tsValidUntil': tsValidUntil.strftime('%Y-%m-%d %H:%M:%S'),
            'ticketNumber': ticketNumber,
            'ownIdentity': ownIdentity,
            'currentNumber': currentNumber,
            'checkSum': checkSum
        }
# --------------- class Functions --------------- #
