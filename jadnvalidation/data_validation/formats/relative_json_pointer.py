from jsonpointer import *

class RelativeJsonPointer:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        RFC 6901 and RFC 6902
        """
        try:

            if not isinstance(self.data, str):
                raise ValueError(f"Invalid JSON pointer, invalid type.  Received {type(self.data)}")
            
            pattern = r"^(0|[1-9][0-9]*)(/[^/]*)?$"
            if not re.fullmatch(pattern, self.data):
                raise ValueError(f"Invalid JSON pointer: {self.data}")

        except ValueError:
            raise ValueError(f"Invalid JSON pointer: {self.data}")