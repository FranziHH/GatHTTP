#!/usr/bin/env python

import sys
# https://www.lambdatest.com/blog/python-configparser-tutorial/
import configparser
import requests
import xml.dom.minidom
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

print ('Config Vars:')
print(url)

try:
    r = requests.get(url, auth=(user, password), timeout=timeout)
except requests.exceptions.Timeout as err:
    print ('timeout')
    sys.exit(0)
except requests.exceptions.HTTPError as err:
    print ('HTTP Error')
    sys.exit(0)
except requests.exceptions.ConnectionError as err:
    print ('Connection Error')
    sys.exit(0)
except requests.exceptions.RequestException as err:
    print ('RequestException Error')
    sys.exit(0)
except Exception as err:
    print ('Other Error')
    sys.exit(0)

if r.status_code != 200:
    print('Status Code:')
    print(r.status_code)
    sys.exit(0)

print(r.text)
dom = xml.dom.minidom.parseString(r.text)

# element = dom.getElementsByTagName('displayText')[0]
try:
    access = getXmlValue(dom, 'access')
except Exception as err:
    # return e.args[0]
    access = "0"

print('access:', access)
print('direction:', getXmlValue(dom, 'direction'))
print('displayText:', getXmlValue(dom, 'displayText').replace("%n", "\n"))
# print('ticketId:', getXmlValue(dom, 'ticketId'))

subprocess.run(['python', 'GatOpen.py', access])
