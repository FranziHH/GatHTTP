from datetime import datetime, timedelta

class offlineBcTypeA:
    def __init__(self, logger):
        self.logger = logger

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

# --------------- class Functions --------------- #
# definition offline Barcode Type A
# https://portalum.atlassian.net/wiki/spaces/C/pages/684490753/TYP+A+Offline+Barcodes

    def decode_barcode(self, barcode: str):
        valid = False
        area = None             # 3 digits
        validUntil = None       # 4 digits
        tsValidUntil = None     # DateTime
        ticketNumber = None     # 2 digits
        ownIdentity = None      # 2 digits
        currentNumber = None    # 5 digits
        checkSum = None         # 2 digits
        calcChecksum = None

        try:
            if len(barcode) >= 16:
                if barcode.isnumeric():
                    area = barcode[0:3]
                    validUntil = barcode[3:7]
                    tsValidUntil = (datetime(2009, 1, 1) + timedelta(days=int(validUntil)) - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
                    ticketNumber = barcode[7:9]
                    ownIdentity = barcode[9:11]
                    currentNumber = barcode[11:16]
                    if len(barcode) == 16:
                        valid = True
                    elif len(barcode) == 18:
                        checkSum = int(barcode[16:18])
                        calcChecksum = self.createCheckSum(barcode)
                        if checkSum == calcChecksum:
                            valid = True

        except Exception as error:
            # raise RuntimeError('config RemoteAccess parameter missing') from error
            print('Error decode_barcode: ' + error.args[0])
            if self.logger is not None:
                self.logger.info('Error decode_barcode: ' + error.args[0])
            self.errMsg = 'Error decode_barcode: ' + error.args[0]
            pass

        return {
            'valid': valid,
            'area': area,
            'validUntil': validUntil,
            'tsValidUntil': tsValidUntil,
            'ticketNumber': ticketNumber,
            'ownIdentity': ownIdentity,
            'currentNumber': currentNumber,
            'checkSum': checkSum,
            'calcChecksum': calcChecksum
        }
    
    def createCheckSum(self, barcode):
        validUntil = int(barcode[3:7])
        currentNumber = int(barcode[11:16])
        return self.checkSum(validUntil) + self.checkSum(currentNumber)
    
    def checkSum(self, value):
        result = 0
        while value:
            result += value % 10
            value = int(value / 10)
        return result
# --------------- class Functions --------------- #
