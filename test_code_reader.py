#!/usr/bin/env python

from classes.ServiceCodeReader import *
import time

reader = ServiceCodeReader()

print(reader.isValid("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR"))

'''
barcode_data = reader.decode_barcode("https://mcdonalds.fast-insight.com/voc/at/de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("de?QRCODE=true&CODE=CC9F-N4GY-K7CC-6CCN-CHTR")
# barcode_data = reader.decode_barcode("CC9F-N4GY-K7CC-6CCN-CHTR")
print(barcode_data)
'''