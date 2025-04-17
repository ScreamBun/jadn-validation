from jsonpointer import *

class JadnJsonPointer:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3387 IRI format.
        """
        try:
            ptr = JsonPointer(self.data).path # need rename to keep this deconflicted from named method
        except ValueError:
            raise ValueError(f"Invalid JSON pointer: {self.data}")