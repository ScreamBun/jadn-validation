from rfc3987 import parse

class IriRef:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 IRI format.
        """
        try:
            # Parse the string using RFC 3387
            parse(self.data, rule='IRI_reference')
        except ValueError:
            raise ValueError(f"Invalid IRI reference: {self.data}")