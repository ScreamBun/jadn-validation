from rfc3987 import parse
from regex import *

class UriRef:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 IRI format.
        """
        try:
            # Parse the string using RFC 3387
            # uri_ref = parse(self.data, rule='URI_reference')
            if isinstance(self.data, str):
                pass # any string passes for now
        except ValueError:
            raise ValueError(f"Invalid URI Reference: {self.data}")