#!/usr/bin/env python

from classes.request import *

req = Request()
req.JsonRequest("TestDevice Mit ÄÖÜ", "12345", "")

retReq = req.JsonRequest("TestDevice Mit ÄÖÜ", "12345", "")
# retReq[0] - Status (True/False)
# retReq[1] - Return Message (Text)
# retReq[2] - Access 0 - False, 1 - True (String)
print(retReq[1])
