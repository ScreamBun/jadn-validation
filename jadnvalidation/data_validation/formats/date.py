from datetime import datetime


class Date:
    
    date: str = None
    date_format: str = "%Y-%m-%d" # String literal RFC 3339 Section 5.6
    errors = []    
    
    def __init__(self, date: any = None):
        self.date = date
    
    def validate(self):
        try:
            datetime.strptime(self.date, self.date_format)
        except ValueError:
            raise ValueError(f"Incorrect date format, should be YYYY-MM-DD: {self.date}")