#!/usr/bin/env python

from functions import *

try:
    req_params = getConfigRequestParams()
except Exception as error:
    print(error.args)
    exit(0)

try:
    xml_string = GetRequest(req_params, '1234', '')
except Exception as error:
    print(error.args)
    exit(0)

print(xml_string)
