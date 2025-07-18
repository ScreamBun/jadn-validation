from datetime import datetime


class Duration:
    
    data: any = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        if isinstance(self.data,str):
            try:
                self.data = int(self.data)
            except ValueError as e:
                print(f"Invalid duration value: {self.data}. Expected an integer / number of seconds.")
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid duration value: {self.data}. Expected an integer / number of seconds.")
        
  