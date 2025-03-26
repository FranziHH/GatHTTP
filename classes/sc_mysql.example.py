import mysql.connector
import atexit

class sc_mysql:
    def __init__(self):
        self.db = mysql.connector.connect(
            host ="<host>",
            user ="<user>",
            passwd ="<password>",
            database = "<database>"
        )
        self.cursor = self.db.cursor()
        atexit.register(self.cleanup)

    def cleanup(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def getDatabase(self):
        self.cursor.execute("select database()")
        return self.cursor.fetchone()[0]
    
    def insertData(self, datas):
        sql = "INSERT INTO sc_entry (created_ts, store_id, pos_id, barcode) VALUES (%s, %s, %s, %s)"
        val = (datas['strDateTime'], datas['storeID'], datas['posID'], datas['barcode'])
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.lastrowid
    
    def updateEntry(self, id, entry):
        sql = "UPDATE sc_entry SET entry = %s WHERE id = %s"
        val = (entry, id)
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.rowcount

    def countEntry(self, bc):
        sql = "SELECT COUNT(id) FROM sc_entry WHERE barcode = %s"
        val = (bc, )
        self.cursor.execute(sql, val)
        res = self.cursor.fetchone()
        return res[0]
    
    def test(self):
        self.cursor.execute("SELECT * FROM sc_entry")
        res = self.cursor.fetchall()

        for x in res:
            print(x)
