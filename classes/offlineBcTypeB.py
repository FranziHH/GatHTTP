import subprocess

class offlineBcTypeB:

    def __init__(self, logger):
        self.logger = logger

    def decode_barcode(self, barcode, key):
        retBC = ''
        valid = None
        cryptType = None
        keyNumber = None
        dataType = None
        placeHolder = None
        separator = None
        data = None
        retData = None

        try:
            # Position des Präfixes "<POE" finden
            prefix_start = barcode.find("<POE") + len("<POE")
            
            # Position des Suffixes "POE>" finden
            suffix_start = barcode.find("POE>", prefix_start)
            
            # Extrahieren des Strings zwischen Präfix und Suffix
            if prefix_start != -1 and suffix_start != -1:
                retBC = barcode[prefix_start:suffix_start]

        except Exception as e:
            pass
        
        # wenn retBC gefüllt ist, config und Daten extrahieren
        try:
            cryptType = int(retBC[0:1])
            keyNumber = int(retBC[1:2])
            dataType = int(retBC[2:4])
            placeHolder = retBC[4:5]
            separator = retBC[5:6]
            data = retBC[6:]
            #Trim Data to right
            trim_start = data.rfind(separator)
            if trim_start != -1:
                data = data[:trim_start]
            
            # simple test to see if data is available at all 
            if len(data) > 20:
                valid = True
        except Exception as e:
            pass
        
        if valid:
            # only continue if no error has occurred up to this point
            print(cryptType, keyNumber, dataType, placeHolder, separator, data)

            match cryptType:
                case 0:
                    #uncrypted
                    retData = data
                case 1:
                    #xor
                    retData = self.xor_encrypt_decrypt(data, key)
                case 2:
                    #AES256
                    retData = self.decode_AES256(data, key)

        return retData
    
    def calculate_xor_checksum_from_string(self, data):
        # Berechnet die XOR-Checksumme für die gegebenen Zeichen eines Strings.
        checksum = 0
        for char in data:
            checksum ^= ord(char)  # Konvertiert Zeichen in ihren ASCII-Wert und XOR
        return checksum

    def xor_encrypt_decrypt(self, data, key):
        # Verschlüsselt oder entschlüsselt einen String mit XOR und einem Schlüssel.
        result = ""
        key_length = len(key)
        
        for i, char in enumerate(data):
            # XOR-Verknüpfung des Zeichens mit dem entsprechenden Schlüsselzeichen
            result += chr(ord(char) ^ ord(key[i % key_length]))
        
        return result

    def decode_AES256(self, data, key):
        valid = False
        barcode = False
        errMsg = None

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
    
        else:
            print('Error decode_barcode: ' + errMsg)
            if self.logger is not None:
                self.logger.info('Error decode_barcode: ' + errMsg)


        return {
            'valid': valid,
            'barcode': barcode,
            'errMsg': errMsg
        }
    