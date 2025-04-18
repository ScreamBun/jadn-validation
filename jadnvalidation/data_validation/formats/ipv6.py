import ipaddress

class Ipv6:
    data = None
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
            except ValueError:
                self.errors.append(f"cannot check value against ipv6 format: {self.data}")
    
    def validate(self):
        """
        Validates if a string matches an ipv6 address.
        """
        try:
            if not ipaddress.IPv6Address(self.data):
                raise ValueError(f"Invalid ipv6 format: {self.data}")
            '''
            match = re.fullmatch("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))", self.string_variable, flags=0)
            if match:
                pass
            else:
                self.errors.append(f"Data does not match ipv6: {self.string_variable}")            
            '''

        except ValueError:
            raise ValueError(f"Invalid ipv6 format: {self.data}")
        
class Ipv6Addr:
    data = None
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
            except ValueError:
                self.errors.append(f"cannot check value against ipv6 format: {self.data}")
    
    def validate(self):
        """
        Validates if a string matches an ipv6 address.
        """
        try:
            if not ipaddress.IPv6Address(self.data): 
                self.errors.append(f"cannot check value against ipv6 format: {self.data}")
            
            '''
            match = re.fullmatch("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))", self.string_variable, flags=0)
            if match:
                pass
            else:
                self.errors.append(f"Data does not match ipv6: {self.string_variable}")            
            '''    

        except ValueError:
            raise ValueError(f"Invalid ipv6 format: {self.data}")