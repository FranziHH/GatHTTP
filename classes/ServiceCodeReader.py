from datetime import datetime

class ServiceCodeReader:
    def __init__(self):
        self.base25_map = {
            0: "C", 1: "M", 2: "7", 3: "W", 4: "D", 5: "6", 6: "N", 7: "4", 8: "R", 9: "H",
            'A': "F", 'B': "9", 'C': "Z", 'D': "L", 'E': "3", 'F': "X", 'G': "K", 'H': "Q", 
            'I': "G", 'J': "V", 'K': "P", 'L': "B", 'M': "T", 'N': "J", 'O': "Y"
        }

    def extract_code(self, input_string):
        if not "mcdonalds" in input_string:
            return ""

        # Überprüfen, ob der gesamte String der Code ist
        if len(input_string) < 24:
            return ""

        if len(input_string) == 24:
            return input_string

        # Extrahiere den Code nach 'CODE='
        if "&CODE=" in input_string:
            start_index = input_string.find("&CODE=") + len("&CODE=")
            output_string = input_string[start_index:]
            if len(output_string) == 24:
                return output_string
            else:
                return "" 

        # Rückgabe für den Fall, dass kein 'CODE=' enthalten ist
        return ""

    def get_map_index(self, value):
        for key, map_value in self.base25_map.items():
            if map_value == value:
                return key
        return 0

    def convert_special_base25_to_base10(self, base25number):
        result = ""
        for character in base25number:
            map_index = self.get_map_index(character)
            result += str(map_index)
        return int(result, 25)

    def delete_additional_chars(self, barcode):
        i = 0
        while i < len(barcode) and barcode[i] == "C":
            i += 1
        return barcode[i:] if i > 0 else barcode

    def isValid(self, barcode):
        return (True, False)[self.extract_code(barcode) == ""]    

    def decode_barcode(self, barcode):
        store_id = None
        pos_id = None
        order_id = None
        amount = None
        sales_type = None
        checker = None
        date_and_time = None
        date_time = None
        stime = None
        
        replaced_string = self.delete_additional_chars(self.extract_code(barcode)).replace("-", "")
        
        if replaced_string != "":

            date_and_time = self.convert_special_base25_to_base10(replaced_string[2:9])
            year = int("20" + str(date_and_time)[:2])
            month_p = int(str(date_and_time)[2:4])
            day_p = int(str(date_and_time)[4:6])
            hour_p = int(str(date_and_time)[6:8])
            min_p = int(str(date_and_time)[8:])

            current_year = datetime.now().year

            if ((current_year - year in [0, 1]) and
                1 <= month_p <= 12 and
                1 <= day_p <= 31 and
                0 <= hour_p <= 23 and
                0 <= min_p < 60 and
                len(str(date_and_time)) == 10):
                store_id = self.convert_special_base25_to_base10(replaced_string[:2])
                sales_type = self.convert_special_base25_to_base10(replaced_string[9:10])
                pos_id = self.convert_special_base25_to_base10(replaced_string[10:12])
                order_id = self.convert_special_base25_to_base10(replaced_string[13:15])
                amount = self.convert_special_base25_to_base10(replaced_string[15:-1])
                checker = replaced_string[-1]
            else:
                store_id = self.convert_special_base25_to_base10(replaced_string[:1])
                date_and_time = self.convert_special_base25_to_base10(replaced_string[1:8])
                sales_type = self.convert_special_base25_to_base10(replaced_string[8:9])
                pos_id = self.convert_special_base25_to_base10(replaced_string[9:11])
                order_id = self.convert_special_base25_to_base10(replaced_string[12:14])
                amount = self.convert_special_base25_to_base10(replaced_string[14:-1])

            date_time = datetime.strptime(str(date_and_time), "%y%m%d%H%M")
            stime = date_time.strftime('%Y-%m-%d %H:%M:%S')

        return {
            'dateTime': date_time,
            'strDateTime': stime,
            'storeID': store_id,
            'posID': pos_id,
            'orderID': order_id,
            'amount': amount,
            'salesType': sales_type,
            'checker': checker,
            'replacedString': replaced_string
        }
