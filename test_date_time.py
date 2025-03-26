#!/usr/bin/env python
from datetime import datetime

# https://www.programiz.com/python-programming/datetime/strftime

stime = "2503031027"

date_time = datetime.strptime(stime, "%y%m%d%H%M")
# date_time = datetime.fromtimestamp(timestamp)
print("DateTime:", date_time)

strTime = date_time.strftime("%d.%m.%Y, %H:%M")
print("Datum:", strTime)
