import mysql.connector
import atexit
import configparser
from datetime import datetime, timedelta

class scMySQL:
    def __init__(self, logger):
        self.active = False
        self.errMsg = ""
        self.logger = logger
        self.config = configparser.ConfigParser()
        self.config.read('datas/config.ini')

        self.getConfigReader()

        if self.active:
            self.db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                database = self.database
            )
            self.cursor = self.db.cursor()
            atexit.register(self.cleanup)

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")
    
    def cleanup(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def getConfigReader(self):
        try:
            self.host = self.config['scReader']['host']
            self.user = self.config['scReader']['user']
            self.passwd = self.config['scReader']['passwd']
            self.database = self.config['scReader']['database']
            self.storeID = int(self.config['scReader']['storeID'])
            self.maxEntrys = int(self.config['scReader']['maxEntrys'])
            self.timeLimit = int(self.config['scReader']['timeLimit'])
            self.timeCleanUp = int(self.config['scReader']['timeCleanUp'])
            self.active = True
        except Exception as error:
            print('config scReader parameter missing')
            if self.logger is not None:
                self.logger.info('config scReader parameter missing')
            self.errMsg = 'config scReader parameter missing'
            pass

        return
    
    def getDatabase(self):
        self.cursor.execute("select database()")
        return self.cursor.fetchone()[0]
    
    def processBarcode(self, datas):
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
        print("----- processBarcode -----")
        print(retData)
        print("----- processBarcode -----")
        if self.logger is not None:
            self.logger.info("----- processBarcode -----")
            self.logger.info(retData)
            self.logger.info("-----")

        return retData

    def insertData(self, datas):
        sql = "INSERT INTO sc_entry (created_ts, store_id, pos_id, barcode, entry, info) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (datas['strDateTime'], datas['storeID'], datas['posID'], datas['barcode'], datas['entry'], datas['info'])
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.lastrowid
    
    def updateEntry(self, id, entry, info):
        sql = "UPDATE sc_entry SET entry = %s, info = %s WHERE id = %s"
        val = (entry, info, id)
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.rowcount

    def countEntrys(self, bc):
        sql = "SELECT COUNT(id) FROM sc_entry WHERE barcode = %s AND entry = 1"
        val = (bc, )
        self.cursor.execute(sql, val)
        return self.cursor.fetchone()[0]
    
    def cleanUP(self):
        tsCleanUP = datetime.now() - timedelta(days=self.timeCleanUp)
        stime = tsCleanUP.strftime('%Y-%m-%d %H:%M:%S')
        sql = "DELETE FROM sc_entry WHERE current_ts < %s"
        val = (stime, )
        self.cursor.execute(sql, val)
        self.db.commit()
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
