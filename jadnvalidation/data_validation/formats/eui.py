from netaddr import EUI


class Eui:
    
    data: any = None
    errors = []    
    
    def __init__(self, data: any = None):
        self.data = data

        if isinstance(self.data, str):
            pass
        elif isinstance(self.data, bytes):   
            self.data = self.data.decode('utf-8')
        else: 
            try:
                self.data = str(self.data)
            except ValueError as e:
                self.errors.append(f"Cannot check value against eui format: {self.data}")
    
    def validate(self):
        """
        Validates if a string matches an EUI with either hyphens or colons.
        """
        try:
            EUI(self.data, None, None)
            
            '''
            match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\\.(?!$)|$)){4}$", self.data, flags=0)
            print(str(match))
            if match:
                pass
            else:
                self.errors.append(f"Data does not match eui: {self.data}")'
                '''
                
        except Exception as err:
            self.errors.append(f"Data does not match eui: {self.data}")
            raise ValueError(err)