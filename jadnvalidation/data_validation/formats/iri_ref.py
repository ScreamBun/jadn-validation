from rfc3987 import parse, _iri_rules

class IriReference:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 IRI format.
        """
        if isinstance(self.data , str) and self.data.__contains__(':'):
            try:
                parse(self.data, rule='IRI_reference')
            except ValueError:
                raise ValueError(f"Invalid IRI reference: {self.data}")        
        else: 
            raise ValueError(f"Invalid URI template: {self.data}")