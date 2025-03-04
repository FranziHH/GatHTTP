#!/usr/bin/env python

from class_request import *

req = Request()
req.JsonRequest("TestDevice Mit ÄÖÜ", "12345", "")

print(req.retStr)
print(req.access)
