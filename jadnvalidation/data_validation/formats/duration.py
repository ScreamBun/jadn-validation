from datetime import datetime


class Duration:
    
    data: any = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid duration value: {self.data}. Expected an integer / number of seconds.")
        
  