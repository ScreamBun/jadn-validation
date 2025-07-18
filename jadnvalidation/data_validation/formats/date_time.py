from datetime import datetime


class DateTime:
    
    # Allow different formats?  See date.py
    date_time: str = None
    
    def __init__(self, date_time: any = None):
        self.date_time = date_time
    
    def validate(self):
        if isinstance(self.date_time, str) and (not self.date_time.lstrip('-').isdigit()):
            try:
                datetime.strptime(self.date_time, self.date_format)
            except ValueError:
                raise ValueError(f"Incorrect date-time format.  Received {self.date_time}")
        else:
            try:
                datetime.fromtimestamp(int(self.date_time))
            except ValueError:
                raise ValueError(f"Invalid timestamp value: {self.date_time}.")