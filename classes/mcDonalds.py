import configparser
from datetime import datetime, timedelta
from classes.mySQL import *


class mcDonalds:
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
            print('mcDonalds: mySQL Init failed!')
            if self.logger is not None:
                self.logger.info('mcDonalds: mySQL Init failed!')
            self.errMsg = 'mcDonalds: mySQL Init failed!'
            return

        self.cursor = self.db.cursor
        self.commit = self.db.commit
        self.getConfig()
        self.mapInit()

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('datas/config.ini')
        try:
            self.active = self.str2bool(config['Modules']['McDonalds'])
            self.storeID = int(config['mcDonalds']['storeID'])
            self.maxEntrys = int(config['mcDonalds']['maxEntrys'])
            self.timeLimit = int(config['mcDonalds']['timeLimit'])
            self.timeCleanUp = int(config['mcDonalds']['timeCleanUp'])
            self.init = True
            if self.init and self.init:
                self.canUse = True
        except Exception as error:
            print('config mcDonalds parameter missing')
            if self.logger is not None:
                self.logger.info('config mcDonalds parameter missing')
            self.errMsg = 'config mcDonalds parameter missing'
            pass

        return

# --------------- Database Functions --------------- #

    def getDatabase(self):
        self.cursor.execute("select database()")
        return self.cursor.fetchone()[0]

    def checkAccess(self, access):
        # Rückmeldung der drehsperre
        # access['procModule'] Check ob es vom eigenen Modul kommt
        # access['accIn'] True/False
        # access['accOut'] True/False

        if self.access == None or self.insertID == None or access['procModule'] != self.__class__.__name__:
            return

        # im Moment wird nur der Zutritt ausgewertet!
        if access['accIn'] == False and self.access:
            # Wenn kein Zutritt erfolgte und ein Zutritt erlaubt war, dann den letzten Eintrag anpassen
            retData = {'entry': 0, 'info': 'no access was reported', 'id': self.insertID}
            self.updateEntry(retData)

            print("----- " + self.__class__.__name__ + ": checkAccess -----")
            print(retData)
            print("-----")
            if self.logger is not None:
                self.logger.info("----- " + self.__class__.__name__ + ": checkAccess -----")
                self.logger.info(retData)
                self.logger.info("-----")

        # nachdem Funktion abgearbeitet wurde, die Daten löschen
        self.access == None
        self.insertID == None

        return

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
                    info = "Access denied: maximum number of accesses exceeded [usedEntrys: " + str(accessCount) + ", maxEntrys: " + str(self.maxEntrys) + "]"
                else:
                    entry = 1
                    info = "Access guaranteed"

        # insert Data into DB
        datas['entry'] = entry
        datas['info'] = info
        self.insertID = self.insertData(datas)

        retData = {'entry': entry, 'info': info, 'insertID': self.insertID}
        print("----- " + self.__class__.__name__ + ": processBarcode -----")
        print(retData)
        print("-----")
        if self.logger is not None:
            self.logger.info("----- " + self.__class__.__name__ + ": processBarcode -----")
            self.logger.info(retData)
            self.logger.info("-----")

        self.access = bool(entry)
        arrBC['access'] = bool(entry)
        arrBC['message'] = info

        return arrBC

    def insertData(self, datas):
        sql = "INSERT INTO mcd_entry (created_ts, store_id, pos_id, barcode, entry, info) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (datas['strDateTime'], datas['storeID'], datas['posID'], datas['barcode'], datas['entry'], datas['info'])
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.lastrowid

    def updateEntry(self, datas):
        sql = "UPDATE mcd_entry SET entry = %s, info = %s WHERE id = %s"
        val = (datas['entry'], datas['info'], datas['id'])
        self.cursor.execute(sql, val)
        self.db.commit()
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
# --------------- Database Functions --------------- #

# --------------- ServiceCode Decode --------------- #
    def mapInit(self):
        self.base25_map = {
            0: "C", 1: "M", 2: "7", 3: "W", 4: "D", 5: "6", 6: "N", 7: "4", 8: "R", 9: "H",
            'A': "F", 'B': "9", 'C': "Z", 'D': "L", 'E': "3", 'F': "X", 'G': "K", 'H': "Q",
            'I': "G", 'J': "V", 'K': "P", 'L': "B", 'M': "T", 'N': "J", 'O': "Y"
        }

    def extract_code(self, input_string):
        # Extrahiere den Code nach 'CODE='
        if "CODE=" in input_string:
            start_index = input_string.rfind("CODE=") + len("CODE=")
            output_string = input_string[start_index:]
            return output_string

        # Rückgabe für den Fall, dass kein 'CODE=' enthalten ist
        return ""

    def get_map_index(self, value):
        for key, map_value in self.base25_map.items():
            if map_value == value:
                return key
        return 0

    def convert_special_base25_to_base10(self, base25number):
        result = ""
        for character in base25number:
            map_index = self.get_map_index(character)
            result += str(map_index)
        return int(result, 25)

    def delete_additional_chars(self, barcode):
        i = 0
        while i < len(barcode) and barcode[i] == "C":
            i += 1
        return barcode[i:] if i > 0 else barcode

    def isValid(self, barcode):
        return (True, False)[self.extract_code(barcode) == ""]

    def decode_barcode(self, barcode):
        store_id = None
        pos_id = None
        order_id = None
        amount = None
        sales_type = None
        checker = None
        date_and_time = None
        date_time = None
        stime = None
        ret_barcode = None

        ret_barcode = self.extract_code(barcode)
        replaced_string = self.delete_additional_chars(ret_barcode).replace("-", "")

        if replaced_string != "":

            date_and_time = self.convert_special_base25_to_base10( replaced_string[2:9])
            year = int("20" + str(date_and_time)[:2])
            month_p = int(str(date_and_time)[2:4])
            day_p = int(str(date_and_time)[4:6])
            hour_p = int(str(date_and_time)[6:8])
            min_p = int(str(date_and_time)[8:])

            current_year = datetime.now().year

            if ((current_year - year in [0, 1]) and
                1 <= month_p <= 12 and
                1 <= day_p <= 31 and
                0 <= hour_p <= 23 and
                0 <= min_p < 60 and
                    len(str(date_and_time)) == 10):
                store_id = self.convert_special_base25_to_base10(replaced_string[:2])
                sales_type = self.convert_special_base25_to_base10(replaced_string[9:10])
                pos_id = self.convert_special_base25_to_base10(replaced_string[10:12])
                order_id = self.convert_special_base25_to_base10(replaced_string[13:15])
                amount = self.convert_special_base25_to_base10( replaced_string[15:-1])
                checker = replaced_string[-1]
            else:
                store_id = self.convert_special_base25_to_base10(replaced_string[:1])
                date_and_time = self.convert_special_base25_to_base10(replaced_string[1:8])
                sales_type = self.convert_special_base25_to_base10(replaced_string[8:9])
                pos_id = self.convert_special_base25_to_base10(replaced_string[9:11])
                order_id = self.convert_special_base25_to_base10(replaced_string[12:14])
                amount = self.convert_special_base25_to_base10(replaced_string[14:-1])

            date_time = datetime.strptime(str(date_and_time), "%y%m%d%H%M")
            stime = date_time.strftime('%Y-%m-%d %H:%M:%S')

        return {
            'dateTime': date_time,
            'strDateTime': stime,
            'storeID': store_id,
            'posID': pos_id,
            'orderID': order_id,
            'amount': amount,
            'salesType': sales_type,
            'checker': checker,
            # 'replacedString': replaced_string,
            'barcode': ret_barcode
        }
# --------------- ServiceCode Decode --------------- #
