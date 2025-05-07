import re

class QName:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        XML Qualified Names are used to represent a URI and local ref pair. QNames are effectively NCNames separated by a colon. 
        """
        if isinstance(self.data , str):
            try:
                if re.fullmatch("^[a-zA-Z_][a-zA-Z-_\.]*[:][a-zA-Z_][a-zA-Z-_\.]*$", self.data, flags=0):
                    pass
                else: 
                    raise ValueError(f"Invalid xml QName: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid xml QName: {self.data}")        
        else: 
            raise ValueError(f"Invalid xml QName: {self.data}")