from jsonpointer import *

class RelativeJsonPointer:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 IRI format.
        """
        try:
            pass # may begin with any valid JSON string... /shrug
            ptr = JsonPointer(self.data).path
        except ValueError:
            raise ValueError(f"Invalid JSON pointer: {self.data}")