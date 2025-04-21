from rfc3987 import parse

class Uri:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 URI format.
        """
        try:
            parse(self.data, rule='URI')
        except ValueError:
            raise ValueError(f"Invalid URI: {self.data}")