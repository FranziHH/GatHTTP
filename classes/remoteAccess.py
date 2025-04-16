import configparser
import requests
import time

class remoteAccess:
    def __init__(self, logger):
        self.active = False
        self.init = False
        self.canUse = False
        self.errMsg = ""
        self.logger = logger
        # ----- wenn der Eintritt nicht vollzogen wird ----- #
        self.access = None
        self.BC = None
        self.RFID = None
        self.lastRequest = None
        # ----- wenn der Eintritt nicht vollzogen wird ----- #
        self.getConfig()

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('datas/config.ini')
        self.url = None
        self.user = None
        self.password = None
        self.timeout = None
        self.GatName = None
        self.lf_replace = None
        
        try:
            self.active = self.str2bool(config['Modules']['RemoteAccess'])
            self.url = config['RemoteAccess']['url']
            self.user = config['RemoteAccess']['username']
            self.password = config['RemoteAccess']['password']
            self.timeout = int(config['RemoteAccess']['timeout'])
            self.GatName = config['RemoteAccess']['GatName']
            self.lf_replace = config['RemoteAccess']['lf_replace'] or ' '
            self.lf_replace = self.lf_replace.replace("\\n", "\n")
            self.init = True
            if self.init and self.init:
                self.canUse = True
        except Exception as error:
            # raise RuntimeError('config RemoteAccess parameter missing') from error
            print('config RemoteAccess parameter missing')
            if self.logger is not None:
                self.logger.info('config RemoteAccess parameter missing')
            self.errMsg = 'config RemoteAccess parameter missing'
            pass

        # ----- Config Read URL Parameters -----
        self.url_barcode = ''
        self.url_rfid = ''
        self.url_params = ''
        param = ''

        for i in range(1, 10):
            try:
                param = config['RemoteAccess']['req_param_' + str(i)]
            except:
                pass
            finally:
                if (param != ''):
                    if (self.url_params == ''):
                        self.url_params = '?'
                    else:
                        self.url_params += '&'

                self.url_params += param
                param = ''

        try:
            self.url_barcode = config['RemoteAccess']['req_barcode']
        except:
            pass

        try:
            self.url_rfid = config['RemoteAccess']['req_rfid']
        except:
            pass

        return

    def JsonRequest(self, GateNo: str, Barcode: str, Rfid: str):
        # retReq[0] - Status (True/False)
        # retReq[1] - Return Message (Text)
        # retReq[2] - Access 0 - False, 1 - True (String)
        self.status = False
        data = {}
        data['GateNo'] = GateNo
        data['Barcode'] = Barcode
        data['Rfid'] = Rfid

        try:
            r = requests.post(self.url, auth=(self.user, self.password), json=data, timeout=self.timeout)
        except requests.exceptions.Timeout as err:
            return {
                'status': False,
                'message': 'Timeout',
                'access': False
            }
        except requests.exceptions.HTTPError as err:
            return {
                'status': False,
                'message': 'HTTP Error',
                'access': False
            }
        except requests.exceptions.ConnectionError as err:
            return {
                'status': False,
                'message': 'Connection Error',
                'access': False
            }
        except requests.exceptions.RequestException as err:
            return {
                'status': False,
                'message': 'RequestException Error',
                'access': False
            }
        except Exception as err:
            return {
                'status': False,
                'message': 'Other Error',
                'access': False
            }

        if (r.status_code == 200):
            try:
                json = r.json()
                retStr = 'access.....: ' + str(json['access']) + "\n"
                retStr += 'direction..: ' + str(json['direction']) + "\n"
                retStr += 'displayText: ' + str(json['displayText']).replace("%n", self.lf_replace)
                return {
                    'status': True,
                    'message': retStr,
                    'access': self.str2bool(json['access'])
                }
            except:
                retStr = "incorrect return data" + "\n"
                retStr += "---------------------" + "\n"
                retStr += r.text
                return {
                    'status': False,
                    'message': retStr,
                    'access': False
                }

        else:
            retStr = "Error Webservice" + "\n"
            retStr += r.status_code
            return {
                'status': False,
                'message': retStr,
                'access': False
            }

    def checkAccess(self, access):
        # Rückmeldung der drehsperre
        # access['procModule'] Check ob es vom eigenen Modul kommt
        # access['accIn'] True/False
        # access['accOut'] True/False

        if self.access == None or access['procModule'] != self.__class__.__name__:
            # anderes Modul aktiv, Daten löschen
            self.BC = None
            self.RFID = None
            self.access = None
            self.lastRequest = None
            return

        # im Moment wird nur der Zutritt ausgewertet!
        if access['accIn'] and self.access:
            # Zutritt erfolgreich, Daten löschen
            self.BC = None
            self.RFID = None
            self.access = None
            self.lastRequest = None

        else:
            # Wenn kein Zutritt erfolgte und ein Zutritt erlaubt war, dann Daten speichern und beim Auswerten des nächsten Scans nutzen
            retData = {'entry': 0, 'info': 'no access was reported', 'BC': self.BC, 'RFID': self.RFID}

            print("----- " + self.__class__.__name__ + ": checkAccess -----")
            print(retData)
            print("-----")
            if self.logger is not None:
                self.logger.info("----- " + self.__class__.__name__ + ": checkAccess -----")
                self.logger.info(retData)
                self.logger.info("-----")

        return
    
    def processBarcode(self, arrBC):
        
        if self.canUse == False or arrBC['recognized']:
            return arrBC

        # Im Falle eines Nicht Zutritts kann durch nochmaliges Scannen jetzt Zutritt erlangt werden ...
        reAccess = False
        if self.access:
            if self.BC != '':
                if self.BC == arrBC['BC']:
                    reAccess = True
            if self.RFID != '':
                if self.RFID == arrBC['RFID']:
                    reAccess = True

            self.BC = None
            self.RFID = None
            self.access = None
            self.lastRequest = None

        if reAccess:
            arrBC['recognized'] = True
            arrBC['access'] = True
            arrBC['message'] = 'do reAccess'
            print(arrBC['message'])
            if self.logger is not None:
                self.logger.info(arrBC['message'])
        else:
            request = self.JsonRequest(self.GatName, arrBC['BC'], arrBC['RFID'])
            # request['status'] - True/False
            # request['message'] - Return Message (Text)
            # request['access'] - True/False
            if (request['status']):
                print(request['message'])
                if self.logger is not None:
                    self.logger.info(request['message'].replace("\n", ", "))
                arrBC['recognized'] = request['access']
                arrBC['access'] = request['access']
                arrBC['message'] = request['message']
            else:
                print('Error: ' + request['message'].replace("\n", ", "))
                if self.logger is not None:
                    self.logger.error(request['message'])
                arrBC['access'] = False
                arrBC['message'] = request['message']
            
        self.BC = arrBC['BC']
        self.RFID = arrBC['RFID']
        self.access = arrBC['access']
        self.lastRequest = time.time()

        arrBC['procModule'] = self.__class__.__name__

        return arrBC
