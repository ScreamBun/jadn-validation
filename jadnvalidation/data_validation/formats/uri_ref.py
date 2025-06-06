from rfc3987 import parse

class UriReference:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 URI format.
        """
        if isinstance(self.data , str) and self.data.__contains__(':'):
            try:
                parse(self.data, rule='URI_reference')
            except ValueError:
                raise ValueError(f"Invalid URI reference: {self.data}")        
        else: 
            raise ValueError(f"Invalid URI reference: {self.data}")