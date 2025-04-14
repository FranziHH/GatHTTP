import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import pkcs7

class Encryption:

    def __init__(self):
        pass

    def Encrypt(self, PlainText, SecurePassword):
        pw_encode = SecurePassword.encode('utf-8')
        text_encode = PlainText.encode('utf-8')

        key = hashlib.sha256(pw_encode).digest()
        iv = Random.new().read(AES.block_size)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        pad_text = pkcs7.encode(text_encode)
        msg = iv + cipher.encrypt(pad_text)

        EncodeMsg = base64.b64encode(msg)
        return EncodeMsg

    def Decrypt(self, Encrypted, SecurePassword):
        decodbase64 = base64.b64decode(Encrypted.decode("utf-8"))
        pw_encode = SecurePassword.decode('utf-8')

        iv = decodbase64[:AES.block_size]
        key = hashlib.sha256(pw_encode).digest()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        msg = cipher.decrypt(decodbase64[AES.block_size:])
        pad_text = pkcs7.decode(msg)

        decryptedString = pad_text.decode('utf-8')
        return decryptedString