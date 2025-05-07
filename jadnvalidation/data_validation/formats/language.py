import re

class Language:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        XML language identifiers are tokens (lacking leading or trailing whitespace) that describe a language the cntent is in.
        Values of the xsd:language type conform to RFC 3066, Tags for the Identification of Languages
        """
        if isinstance(self.data , str):
            try:
                if re.fullmatch("^[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*$", self.data, flags=0):
                    pass
                else: 
                    raise ValueError(f"Invalid xml language identifier: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid xml language identifier: {self.data}")        
        else: 
            raise ValueError(f"Invalid xml language identifier: {self.data}")