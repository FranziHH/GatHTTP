import mysql.connector
import atexit
import configparser

class mySQL:
    def __init__(self, logger):
        self.init = False
        self.errMsg = ""
        self.logger = logger
        self.config = configparser.ConfigParser()
        self.config.read('datas/config.ini')
        self.db = None
        self.cursor = None
        self.commit = None

        self.getConfigReader()

        if self.init:
            self.db = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                database = self.database
            )
            self.cursor = self.db.cursor()
            self.commit = self.db.commit()
            atexit.register(self.cleanup)

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")
    
    def cleanup(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def getConfigReader(self):
        try:
            self.host = self.config['Database']['host']
            self.user = self.config['Database']['user']
            self.passwd = self.config['Database']['passwd']
            self.database = self.config['Database']['database']
            self.init = True
        except Exception as error:
            print('config mySQL parameter missing')
            if self.logger is not None:
                self.logger.info('config mySQL parameter missing')
            self.errMsg = 'config mySQL parameter missing'
            pass

        return
    
    def getDatabase(self):
        self.cursor.execute("select database()")
        return self.cursor.fetchone()[0]
    
