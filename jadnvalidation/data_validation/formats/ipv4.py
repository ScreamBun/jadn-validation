import ipaddress

class Ipv4:
    data: bytes = None
    data_str: str = None
    errors = []    
    
    def __init__(self, data: any = None):
        self.data = data

        if isinstance(self.data, str):
            self.data_str = data
            print(self.data_str)
        elif isinstance(self.data, bytes):   
            self.data_str = self.data.decode('utf-8')
            print(self.data_str)
        else: 
            print(str(self.data))
            try:
                self.data_str = str(self.data)
            except ValueError as e:
                self.errors.append(f"cannot check value against ipv4 format: {self.data}")
            #self.errors.append(f"Data does not match ipv6: {self.string_variable}")
    
    def validate(self):
        """
        Validates if a string matches an ipv4 address.
        """
        try:
            assert ipaddress.IPv4Address(self.data)
            '''
            match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$", self.data_str, flags=0)
            if match:
                pass
            else:
                self.errors.append(f"Data does not match ipv4: {self.data_str}")'
                '''
        except ValueError:
            raise ValueError(f"Invalid ipv4 format: {self.data_str}")
        
class Ipv4Addr:
    data: bytes = None
    data_str: str = None
    errors = []    
    
    def __init__(self, data: any = None):
        self.data = data

        if isinstance(self.data, str):
            self.data_str = data
            print(self.data_str)
        elif isinstance(self.data, bytes):   
            self.data_str = self.data.decode('utf-8')
            print(self.data_str)
        else: 
            print(str(self.data))
            try:
                self.data_str = str(self.data)
            except ValueError as e:
                self.errors.append(f"cannot check value against ipv4 format: {self.data}")
            #self.errors.append(f"Data does not match ipv6: {self.data_str}")
    
    def validate(self):
        """
        Validates if a string matches an ipv4 address.
        """
        try:
            assert ipaddress.IPv4Address(self.data_str)
            '''
            match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$", self.data_str, flags=0)
            if match:
                pass
            else:
                self.errors.append(f"Data does not match ipv4: {self.data_str}")'
                '''
        except ValueError:
            raise ValueError(f"Invalid ipv4 address format: {self.data}")