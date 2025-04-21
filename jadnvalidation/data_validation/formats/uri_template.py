import uri_template

class UriTemplate:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 URI template format.
        """
        if isinstance(self.data , str) and self.data.__contains__('{'):
            try:                
                if not uri_template.validate(self.data):
                    raise ValueError(f"Invalid URI template: {self.data}")
            except ValueError:
                raise ValueError(f"Invalid URI template: {self.data}")
        else: 
            raise ValueError(f"Invalid URI template: {self.data}")