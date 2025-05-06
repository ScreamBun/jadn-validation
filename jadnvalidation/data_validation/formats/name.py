import re

class Name:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        XML names conform to certain charracteristics.
        """
        if isinstance(self.data , str):
            try:
                if re.fullmatch("^[a-zA-Z_:][a-zA-Z-_:\.]*$", self.data, flags=0):
                    pass
                else: 
                    raise ValueError(f"Invalid xml name: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid xml name: {self.data}")        
        else: 
            raise ValueError(f"Invalid xml name: {self.data}")