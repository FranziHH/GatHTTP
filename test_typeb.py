#!/usr/bin/env python
from classes.offlineBcTypeB import *

cOfflineBcTypeB = offlineBcTypeB(None)

print(cOfflineBcTypeB.sslVersion())
exit()

data = '<POE24000#U2FsdGVkX192o+97fs4Ab6YQOJFuh+aFzsix9qFWH6qUnS4CsNtUMRK9QprvXbCDF4UwPoRT+5sOahJ4eDU4XTlz1ZEDLUzvazFIMKiYEiqotpJyAtm2++TZ0sJUa7t1xSWkZ31dPuECi1VQQGQ8+Jz/kh6xVL5CkAShR5mTecw=#POE>'
key = 'PortalumSuperGeheimesPasswort12345'

# print(cOfflineBcTypeB.decode_barcode(data, key))
3#12#25.05.2020 14:30#26.05.2020 18:30#196.0005#141#2#DominikGregotsch#Pretix#1457152124454545145#2E


ret = cOfflineBcTypeB.xor_encrypt_decrypt('3#12#25.05.2020 14:30#26.05.2020 18:30#196.0005#141#2#DominikGregotsch#Pretix#1457152124454545145#2E', key)
ret = cOfflineBcTypeB.xor_encrypt_decrypt(ret, key)
print(ret)
