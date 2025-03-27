#!/usr/bin/env python

from classes.scReader import *
from classes.scMySQL import *

reader = scReader()
myDB = scMySQL(None)

if not myDB.active:
    print("scReader isn't activated!")
    exit()


# print(reader.isValid("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR"))

'''
barcode_data = reader.decode_barcode("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("CC9F-N4GY-K7CC-6CCN-CHTR")
print(barcode_data)
'''

barcode_data = reader.decode_barcode("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")

print(myDB.processBarcode(barcode_data))
exit()

lastID = myDB.insertData(barcode_data)
print(lastID)

myDB.updateEntry(lastID, 1)

# myDB.test()

print(myDB.countEntrys('CC9F-N4GY-K7CC-6CCN-CHTR'))

# print(myDB.storeID)
