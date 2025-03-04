from func_main import *
import sys
import requests

class Request:
    def __init__(self):
        try:
            cfgReq = getConfigRequestParams()
        except Exception as error:
            print(error.args)
            exit(0)

        self.retStr = ""
        self.status = False
        self.access = ""

        self.url = cfgReq[0]
        self.user = cfgReq[1]
        self.password = cfgReq[2]
        self.timeout = cfgReq[3]
        self.url_params = cfgReq[4]
        self.url_barcode = cfgReq[5]
        self.url_rfid = cfgReq[6]


    def JsonRequest(self, GateNo: str, Barcode: str, Rfid: str):
        self.status = False
        data = {}
        data['GateNo'] = GateNo
        data['Barcode'] = Barcode
        data['Rfid'] = Rfid

        try:
            # r = requests.post(url, auth=(user, password), data=data, timeout=timeout)
            r = requests.post(self.url, auth=(self.user, self.password), json=data, timeout=self.timeout)
        except requests.exceptions.Timeout as err:
            self.retStr = 'timeout'
            return self.status
        except requests.exceptions.HTTPError as err:
            self.retStr = 'HTTP Error'
            return self.status
        except requests.exceptions.ConnectionError as err:
            self.retStr = 'Connection Error'
            return self.status
        except requests.exceptions.RequestException as err:
            self.retStr = 'RequestException Error'
            return self.status
        except Exception as err:
            self.retStr = 'Other Error'
            return self.status


        if (r.status_code == 200):
            try:
                json = r.json()
                self.retStr = 'access.....: ' + str(json['access']) + "\n"
                self.retStr += 'direction..: ' + str(json['direction']) + "\n"
                self.retStr += 'displayText: ' + str(json['displayText']).replace("%n", " <br> ")
                # open gate
                self.status = True
                self.access = str(json['access'])
                # subprocess.run(['python', 'GatOpen.py', str(json['access'])])
                return self.status
            except:
                self.retStr = "incorrect return data" + "\n"
                self.retStr += "---------------------" + "\n"
                self.retStr += r.text
                return self.status

        else:
            self.retStr = "Error Webservice" + "\n"
            self.retStr += r.status_code
            return self.status
