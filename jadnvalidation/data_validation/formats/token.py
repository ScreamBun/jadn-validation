import re

class Token:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        XML tokens lack leading or trailing whitespace.
        """
        if isinstance(self.data , str):
            try:
                if re.fullmatch("^\S+(?:\s+\S+)*$", self.data, flags=0):
                    pass
                else: 
                    raise ValueError(f"Invalid xml token: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid xml token: {self.data}")        
        else: 
            raise ValueError(f"Invalid xml token: {self.data}")