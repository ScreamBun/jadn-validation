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
                # Parse the string using RFC 3387
                #uri = get_compiled_pattern ('^%(URI)s$')
                #print(self.data)
                assert uri_template.validate(self.data)
            except ValueError:
                raise ValueError(f"Invalid URI template: {self.data}")
        else: 
            raise ValueError(f"Invalid URI template: {self.data}")