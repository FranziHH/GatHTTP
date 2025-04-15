#!/usr/bin/env python
from classes.offlineBcTypeB import *

cOfflineBcTypeB = offlineBcTypeB(None)

'''
print(cOfflineBcTypeB.sslVersion())
exit()
'''

# Zutritt
data = '<POE24000#U2FsdGVkX192o+97fs4Ab6YQOJFuh+aFzsix9qFWH6qUnS4CsNtUMRK9QprvXbCDF4UwPoRT+5sOahJ4eDU4XTlz1ZEDLUzvazFIMKiYEiqotpJyAtm2++TZ0sJUa7t1xSWkZ31dPuECi1VQQGQ8+Jz/kh6xVL5CkAShR5mTecw=#POE>'

# Access Type 2
data = '<POE21000#U2FsdGVkX1/wUnTYc2MVdK2mltz+xdx0EzLpOy9T0waulmXt3pRuganD4UxVMZqcEg7/ykeMtEhNmgtXXzit9ex90mq8Ojg7yuSgZR5Uu+5a544kdw0H8N1Rzmh8hgScHN2FCevz0oTsFezKcJ/nfg==#POE>'

# Course
data = '<POE23010#U2FsdGVkX1/jx7fKnzJ5ChP2xdgN3WdHpR1WkLj5bZsXsyACvxfTiCZI680RBi2z6YEI2eeLqARfIHhGgF6s2w==#POE>'


keyArr = ['supergeheim',
          '',
          'supergeheim',
          'PortalumSuperGeheimesPasswort12345',
          '',
          '',
          '',
          '',
          ''
        ]

retData = cOfflineBcTypeB.decode_barcode(data, keyArr)
if retData['valid']:
    bcArr = cOfflineBcTypeB.assignData(retData['data'], retData['dataType'])
    print(bcArr)
else:
    print('Function Error', retData['errMsg'])



# 3#12#25.05.2020 14:30#26.05.2020 18:30#196.0005#141#2#DominikGregotsch#Pretix#1457152124454545145#2E

'''
ret = cOfflineBcTypeB.xor_encrypt_decrypt('3#12#25.05.2020 14:30#26.05.2020 18:30#196.0005#141#2#DominikGregotsch#Pretix#1457152124454545145#2E', keyArr[3])
print(ret['barcode'])
ret = cOfflineBcTypeB.xor_encrypt_decrypt(ret['barcode'], 'test')
print(ret)
'''