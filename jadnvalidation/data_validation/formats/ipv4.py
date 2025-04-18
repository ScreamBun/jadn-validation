import ipaddress

class Ipv4:
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
                self.errors.append(f"cannot check value against ipv4 format: {self.data}")
    
    def validate(self):
        """
        Validates if a string matches an ipv4 address.
        """
        try:
            if not ipaddress.IPv4Address(self.data):
                raise ValueError(f"Invalid ipv4 format: {self.data}")
            '''
            match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$", self.data, flags=0)
            if match:
                pass
            else:
                self.errors.append(f"Data does not match ipv4: {self.data}")'
                '''
        except ValueError:
            raise ValueError(f"Invalid ipv4 format: {self.data}")
        
class Ipv4Addr:
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
                self.errors.append(f"cannot check value against ipv4 format: {self.data}")
    
    def validate(self):
        """
        Validates if a string matches an ipv4 address.
        """
        try:
            if not ipaddress.IPv4Address(self.data): 
                self.errors.append(f"cannot check value against ipv4 format: {self.data}")
            '''
            match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$", self.data_str, flags=0)
            if match:
                pass
            else:
                self.errors.append(f"Data does not match ipv4: {self.data_str}")'
                '''
        except ValueError:
            raise ValueError(f"Invalid ipv4 address format: {self.data}")