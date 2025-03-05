import configparser
import requests


class Request:
    def __init__(self):
        try:
            self.getConfigRequestParams()
        except Exception as error:
            print(error.args)
            exit(0)

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def getConfigRequestParams(self):
        config = configparser.ConfigParser()
        config.read('datas/config.ini')

        try:
            self.url = config['Request']['url']
            self.user = config['Request']['username']
            self.password = config['Request']['password']
            self.timeout = int(config['Request']['timeout'])
            self.lf_replace = config['Request']['lf_replace'] or ' '
            self.lf_replace = self.lf_replace.replace("\\n", "\n")
        except Exception as error:
            raise RuntimeError('config Request parameter missing') from error

        # ----- Config Read URL Parameters -----
        self.url_barcode = ''
        self.url_rfid = ''
        self.url_params = ''
        param = ''

        for i in range(1, 10):
            try:
                param = config['Request']['req_param_' + str(i)]
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
            self.url_barcode = config['Request']['req_barcode']
        except:
            pass

        try:
            self.url_rfid = config['Request']['req_rfid']
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
            return [False, 'Timeout', '0']
        except requests.exceptions.HTTPError as err:
            return [False, 'HTTP Error', '0']
        except requests.exceptions.ConnectionError as err:
            return [False, 'Connection Error', '0']
        except requests.exceptions.RequestException as err:
            return [False, 'RequestException Error', '0']
        except Exception as err:
            return [False, 'Other Error', '0']

        if (r.status_code == 200):
            try:
                json = r.json()
                retStr = 'access.....: ' + str(json['access']) + "\n"
                retStr += 'direction..: ' + str(json['direction']) + "\n"
                retStr += 'displayText: ' + str(json['displayText']).replace("%n", self.lf_replace)
                return [True, retStr, str(json['access'])]
            except:
                retStr = "incorrect return data" + "\n"
                retStr += "---------------------" + "\n"
                retStr += r.text
                return [False, retStr, '0']

        else:
            retStr = "Error Webservice" + "\n"
            retStr += r.status_code
            return [False, retStr, '0']
