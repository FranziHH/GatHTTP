#!/usr/bin/env python

import sys
# https://www.lambdatest.com/blog/python-configparser-tutorial/
import configparser
import requests
from functions import *
import subprocess

config = configparser.ConfigParser()
config.read('config.ini')

# print(config.sections())
try:
    url = config['Request']['url']
    user = config['Request']['username']
    password = config['Request']['password']
    timeout = int(config['Request']['timeout'])
except Exception as err:
    print("config parameter missing")
    sys.exit(0)

print('Config Vars:')
print(url)

data = {}
data['GateNo'] = "TestDevice"
data['Barcode'] = "12345"
data['Rfid'] = ""

try:
    # r = requests.post(url, auth=(user, password), data=data, timeout=timeout)
    r = requests.post(url, auth=(user, password), json=data, timeout=timeout)
except requests.exceptions.Timeout as err:
    print('timeout')
    sys.exit(0)
except requests.exceptions.HTTPError as err:
    print('HTTP Error')
    sys.exit(0)
except requests.exceptions.ConnectionError as err:
    print('Connection Error')
    sys.exit(0)
except requests.exceptions.RequestException as err:
    print('RequestException Error')
    sys.exit(0)
except Exception as err:
    print('Other Error')
    sys.exit(0)


if (r.status_code == 200):
    try:
        json = r.json()
        print('access.....:', str(json['access']))
        print('direction..:', str(json['direction']))
        print('displayText:', str(json['displayText']))
        # open gate
        subprocess.run(['python', 'GatOpen.py', str(json['access'])])
    except:
        print("incorrect return data")
        print("---------------------")
        print(r.text)

else:
    print("Error Webservice")
    print(r.status_code)
