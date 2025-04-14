#!/usr/bin/env python
import base64
import urllib2
from Crypto.Cipher import AES


def decrypt(quotedEncodedEncrypted):
    key = 'SecretKey'

    encodedEncrypted = urllib2.unquote(quotedEncodedEncrypted)

    cipher = AES.new(key)
    decrypted = cipher.decrypt(base64.b64decode(encodedEncrypted))[:16]

    for i in range(1, len(base64.b64decode(encodedEncrypted))/16):
        cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(encodedEncrypted)[(i-1)*16:i*16])
        decrypted += cipher.decrypt(base64.b64decode(encodedEncrypted)[i*16:])[:16]

    return decrypted.strip()