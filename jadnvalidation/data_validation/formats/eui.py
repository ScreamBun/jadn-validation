from netaddr import *

class Eui:
    
    data_str: str = ""
    data: bytes = None
    errors = []    
    
    def __init__(self, data: any = None):
        self.data = data

        if isinstance(self.data, str):
            self.data_str = data
            print('str'+self.data_str)
        elif isinstance(self.data, bytes):   
            self.data_str = self.data.decode('utf-8')
            print('bytes'+self.data_str)
        else: 
            print(str(self.data))
            try:
                self.data_str = str(self.data)
            except ValueError as e:
                self.errors.append(f"cannot check value against eui format: {self.data}")
            #self.errors.append(f"Data does not match eui: {self.string_variable}")
    
    def validate(self):
        """
        Validates if a string matches an EUI with either hyphens or colons.
        """
        try:
            assert valid_eui64(self.data_str)
            '''
            match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\\.(?!$)|$)){4}$", self.data_str, flags=0)
            print(str(match))
            if match:
                pass
            else:
                self.errors.append(f"Data does not match eui: {self.data_str}")'
                '''
        except Exception as err:
            self.errors.append(f"Data does not match eui: {self.data_str}")
            raise ValueError(err)