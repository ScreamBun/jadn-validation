import ipaddress

class Ipv6:
    data = None
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
                self.errors.append(f"cannot check value against ipv6 format: {self.data}")
            #self.errors.append(f"Data does not match ipv6: {self.string_variable}")
    
    def validate(self):
        """
        Validates if a string matches an ipv6 address.
        """
        try:
            assert ipaddress.IPv6Address(self.data_str)
            #match = re.fullmatch("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))", self.string_variable, flags=0)
            #if match:
                #pass
            #else:
                #self.errors.append(f"Data does not match ipv6: {self.string_variable}")
        except ValueError:
            raise ValueError(f"Invalid ipv6 format: {self.data_str}")
        
class Ipv6Addr:
    data = None
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
                self.errors.append(f"cannot check value against ipv6 format: {self.data}")
            #self.errors.append(f"Data does not match ipv6: {self.string_variable}")
    
    def validate(self):
        """
        Validates if a string matches an ipv6 address.
        """
        try:
            assert ipaddress.IPv6Address(self.data_str)
            #match = re.fullmatch("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))", self.string_variable, flags=0)
            #if match:
                #pass
            #else:
                #self.errors.append(f"Data does not match ipv6: {self.string_variable}")
        except ValueError:
            raise ValueError(f"Invalid ipv6 format: {self.data_str}")