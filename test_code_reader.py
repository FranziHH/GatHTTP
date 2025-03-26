#!/usr/bin/env python

from classes.ServiceCodeReader import *
from classes.sc_mysql import *

reader = ServiceCodeReader()
myDB = sc_mysql()

# print(reader.isValid("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR"))

'''
barcode_data = reader.decode_barcode("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("CC9F-N4GY-K7CC-6CCN-CHTR")
print(barcode_data)
'''

'''
barcode_data = reader.decode_barcode("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
lastID = myDB.insertData(barcode_data)
print(lastID)

myDB.updateEntry(lastID, 1)

myDB.test()
'''

print(myDB.countEntry('CC9F-N4GY-K7CC-6CCN-CHTR'))
