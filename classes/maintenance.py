import base64

class maintenance:
    def __init__(self):
        self.data = [
            b'MTYxNDIzNzg4MDgyOTc2NzQ1OTk=',
            b'MTYxNDIzNzg4MDgyOTc4MjQ4ODU=',
            b'MTYxNDIzNzg4MDgyOTc3MzcwMDQ=',
            b'MTYxNDIzNzg4MDgyOTc3OTc5MTA=',
            b'MTYxNDIzNzg4MDgyOTc4MjUxMDY=',
            b'MzUzMTE3MjY0',
            # Portalum
            b'NDY0NTc4NjU2ODU1MTE1MzQ4NDU1MDczMDI0NDY2MTg0NTQzMTc5NDMyODk2ODIwMzkyMjMxNTkxODQ2ODg0NzM2',
            b'MTI0MTcwOTQzOTEwNDM4NA==',
            b'MTEzNzIwODA1ODY1NjM4NA==',
            b'MTE0ODA4NzIxMDgxNzE1Mg==',
            b'MTI2OTE4NDM0NDg5Njg5Ng==',
            b'MTI3Nzg1MjUzMzczMDY4OA==',
            b'MTIwNTY4NTk0NjQyOTMxMg==',
            b'MTE4ODExMDk0MDI1NDA4MA=='
        ]

    def processBarcode(self, arrBC):
        if not arrBC['recognized']:
            if arrBC['RFID'] != "":
                if base64.b64encode(arrBC['RFID'].encode()) in self.data:
                    arrBC['recognized'] = True
                    arrBC['access'] = True
                    arrBC['procModule'] = self.__class__.__name__
                    arrBC['message'] = ''

        return arrBC
