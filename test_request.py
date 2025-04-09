#!/usr/bin/env python

from classes.gatHttp import *

gatHttp = gatHttp(None)
gatHttp.JsonRequest("TestDevice Mit ÄÖÜ", "12345", "")

request = gatHttp.JsonRequest("TestDevice Mit ÄÖÜ", "12345", "")
# retReq[0] - Status (True/False)
# retReq[1] - Return Message (Text)
# retReq[2] - Access 0 - False, 1 - True (String)
print(request[1])
