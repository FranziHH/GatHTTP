#!/usr/bin/env python
from classes.logger import *
from classes.mcDonalds import *

# ----- Init Logger ----- #
cLogger = logger(os.path.basename(__file__)).logger
# ----- Init Logger ----- #

# ----- Init mcDonalds ----- #
isMcDonalds = True
cMcDonalds = mcDonalds(cLogger)

if not cMcDonalds.active:
    print("McDonalds isn't activated!")
    cLogger.info("McDonalds isn't activated!")
    isMcDonalds = False

if not cMcDonalds.init:
    print("McDonalds Settings failed!")
    cLogger.info("McDonalds Settings failed!")
    isMcDonalds = False
# ----- Init mcDonalds ----- #

if not isMcDonalds:
    exit()

# print(reader.isValid("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR"))

'''
barcode_data = reader.decode_barcode("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("CC9F-N4GY-K7CC-6CCN-CHTR")
print(barcode_data)
'''

barcode_data = cMcDonalds.decode_barcode("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")

print(cMcDonalds.processBarcode(barcode_data))
exit()

lastID = cMcDonalds.insertData(barcode_data)
print(lastID)

cMcDonalds.updateEntry(lastID, 1)

# cMcDonalds.test()

print(cMcDonalds.countEntrys('CC9F-N4GY-K7CC-6CCN-CHTR'))

# print(cMcDonalds.storeID)
