import re

class NormalizedString:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        XML normalized strings conform to certain charracteristics.
        """
        if isinstance(self.data , str):
            try:
                if re.fullmatch("^[\S]*$", self.data, flags=0):
                    pass
                else: 
                    raise ValueError(f"Invalid xml normalized string: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid xml normalized string: {self.data}")        
        else: 
            raise ValueError(f"Invalid xml normalized string: {self.data}")