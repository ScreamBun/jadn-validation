from datetime import datetime

from jadnvalidation.utils.consts import DATE_FORMAT


class Date:
    
    date: str = None
    date_format: str = DATE_FORMAT # RFC 3339 Date Format
    
    def __init__(self, date: any = None):
        self.date = date
    
    def validate(self):
        if isinstance(self.date, str):
            try:
                datetime.strptime(self.date, self.date_format)  
            except ValueError:
                raise ValueError(f"Incorrect date format, should be {self.date_format}.  Recieved {self.date}")
        elif isinstance(self.date, int):
            try:
                datetime.fromtimestamp(self.date)
            except ValueError:
                raise ValueError(f"Invalid timestamp value: {self.date}.")
        else:
            raise ValueError(f"Date must be a string or an integer (timestamp). Received: {type(self.date)}")