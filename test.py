#!/usr/bin/env python

# https://www.lambdatest.com/blog/python-configparser-tutorial/
import configparser
import requests
import xml.dom.minidom

config = configparser.ConfigParser()
config.read('config.ini')

def getXmlValue(node):
    try:
        return dom.getElementsByTagName(node)[0].firstChild.nodeValue
    except Exception as e:
        # return e.args[0]
        return "ERROR"


# print(config.sections())
req_url = config['request']['url']

print ('Config Vars:')
print(req_url)

r = requests.get(req_url)
# print('Status Code:')
# print(r.status_code)

print(r.text)
dom = xml.dom.minidom.parseString(r.text)

# element = dom.getElementsByTagName('displayText')[0]
print('access:', getXmlValue('access'))
print('direction:', getXmlValue('direction'))
print('displayText:', getXmlValue('displayText').replace("%n", "\n"))
# print('ticketId:', getXmlValue('ticketId'))
