import subprocess

# definition offline Barcode Type A
# https://portalum.atlassian.net/wiki/spaces/C/pages/207814665/Typ+B+neue+Portalum+QR+Codes

class offlineBcTypeB:

    def __init__(self, logger):
        self.logger = logger

    def decode_barcode(self, barcode, keyArr):
        retBC = ''
        valid = None
        cryptType = None
        keyNumber = None
        dataType = None
        placeHolder = None
        separator = None
        data = None
        retData = None
        retArr = None
        checkSum = None
        calcChecksum = None
        errMsg = ''

        try:
            # Position des Präfixes "<POE" finden
            prefix_start = barcode.find("<POE") + len("<POE")

            # Position des Suffixes "POE>" finden
            suffix_start = barcode.find("POE>", prefix_start)

            # Extrahieren des Strings zwischen Präfix und Suffix
            if prefix_start != -1 and suffix_start != -1:
                retBC = barcode[prefix_start:suffix_start]
            else:
                if errMsg != '': errMsg += '\n'
                errMsg += 'prefix / postfix not found'

        except Exception as e:
            if errMsg != '': errMsg += '\n'
            errMsg += 'Error: prefix / postfix'
            pass

        # wenn retBC gefüllt ist, config und Daten extrahieren
        try:
            cryptType = int(retBC[0:1])
            keyNumber = int(retBC[1:2])
            dataType = int(retBC[2:4])
            placeHolder = retBC[4:5]
            separator = retBC[5:6]
            data = retBC[6:]
            # Trim Data to right
            trim_start = data.rfind(separator)
            if trim_start != -1:
                data = data[:trim_start]

            # simple test to see if data is available at all
            if len(data) > 20:
                valid = True
            else:
                if errMsg != '': errMsg += '\n'
                errMsg += 'wrong data len: ' + len(data)

            # es wird nur der Datentyp = 0 (Zutritts Ticket) verarbeitet!
            if dataType != 0:
                if errMsg != '': errMsg += '\n'
                errMsg += 'wrong dataType: ' + dataType
                valid = False

        except Exception as e:
            if errMsg != '': errMsg += '\n'
            errMsg += 'Error Barcode: ' + str(e)
            pass
        
        if len(keyArr) == 9:
            key = keyArr[keyNumber - 1]
        else:
            valid = False
            if errMsg != '': errMsg += '\n'
            errMsg += 'wrong keyArray'
        
        if valid:
            # only continue if no error has occurred up to this point
            # print(cryptType, keyNumber, dataType, placeHolder, separator, data)

            match cryptType:
                case 0:
                    # uncrypted
                    retData = data
                case 1:
                    # xor
                    retData = self.xor_encrypt_decrypt(data, key)
                case 2:
                    # AES256
                    retTmp = self.decode_AES256(data, key)
                    valid = retTmp['valid']
                    retData = retTmp['barcode']
                    if retTmp['errMsg'] != '':
                        if errMsg != '': errMsg += '\n'
                        errMsg += retTmp['errMsg']
            
            calcChecksum = self.calculate_xor_checksum_from_string(retData[:-2])
            checkSum = retData[-2:]
            if checkSum != calcChecksum:
                valid = False
                if errMsg != '': errMsg += '\n'
                errMsg += 'checksum does not match'

            retArr = str(retData).split(separator)
            
        return {
            'valid': valid,
            'cryptType': cryptType,
            'keyNumber': keyNumber,
            'dataType': dataType,
            'placeHolder': placeHolder,
            'separator': separator,
            'data': retArr,
            'checkSum': checkSum,
            'calcChecksum': calcChecksum,
            'errMsg': errMsg
        }

    def assignData(self, data, type):
        # im Moment wird nur der Typ 0 verarbeitet!
        retData = None

        match type:
            case 0:
                if len(data) >= 10:
                    retData = {
                        'version': data[0],
                        'type': data[1],
                        'validFrom': data[2],
                        'validTo': data[3],
                        'reference': data[4],
                        'area': data[5],
                        'location': data[6],
                        'owner': data[7],
                        'origin': data[8],
                        'ticketId': data[9],
                    }
            case _:
                pass
        
        return retData


    def calculate_xor_checksum_from_string(self, data):
        # Berechnet die XOR-Checksumme für die gegebenen Zeichen eines Strings.
        checksum = 0
        retStr = '--'

        try:
            for char in data:
                # Konvertiert Zeichen in ihren ASCII-Wert und XOR
                checksum ^= ord(char)

            retStr = f'{checksum:x}'.upper()

        except Exception as e:
            pass

        return retStr

    def xor_encrypt_decrypt(self, data, key):
        # Verschlüsselt oder entschlüsselt einen String mit XOR und einem Schlüssel.
        valid = False
        barcode = ''
        errMsg = ''

        key_length = len(key)

        for i, char in enumerate(data):
            # XOR-Verknüpfung des Zeichens mit dem entsprechenden Schlüsselzeichen
            barcode += chr(ord(char) ^ ord(key[i % key_length]))

        return {
            'valid': valid,
            'barcode': barcode,
            'errMsg': errMsg
        }

    def decode_AES256(self, data, key):
        valid = False
        barcode = None
        errMsg = ''

        try:
            command = f"echo '{data}' | openssl enc -d -base64 -aes-256-cbc -pbkdf2 -salt -k '{key}'"
            process = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if process.returncode != 0:
                # Kompletten Fehlertext
                full_error = process.stderr.decode()

                # Nur "bad decrypt" extrahieren
                if "bad decrypt" in full_error:
                    errMsg = 'bad decrypt'

                errMsg = full_error.strip()

            valid = True

        except Exception as e:
            errMsg = 'Error decode_barcode: ' + str(e)
            pass

        if valid:
            try:
                barcode = process.stdout.decode().rstrip("\r\n")

            except Exception as e:
                valid = False
                errMsg = 'Error decode_barcode: ' + str(e)
                pass

        if not valid:
            print('Error decode_barcode: ' + errMsg)
            if self.logger is not None:
                self.logger.info('Error decode_barcode: ' + errMsg)

        return {
            'valid': valid,
            'barcode': barcode,
            'errMsg': errMsg
        }

    def sslVersion(self):
        try:
            command = f"openssl version"
            process = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if process.returncode != 0:
                return process.stderr.decode().strip()

            return process.stdout.decode().strip()

        except Exception as e:
            return 'Error sslVersion: ' + str(e)
