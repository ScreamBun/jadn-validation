from iso8601 import iso8601
from datetime import datetime     
        
class GYear:
    
    # Allow different formats?  See date.py
    date_str: str = None
    data_int: int = None
    datetime_converted: datetime = None
    
    def __init__(self, date_entry: any = None):
        if isinstance(date_entry, str):
            self.date_str = date_entry
        elif isinstance(date_entry, int):
            self.date_int = date_entry
            self.date_str = str(self.date_int)
        else:
            raise ValueError(f"Invalid date-time format: {date_entry}")
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3339 date-time format.
        """
        try:
            # Parse the string using ISO 8601 format
            datetime_converted = iso8601.parse_date(self.date_str)
        except ValueError:
            raise ValueError(f"Invalid date-time format: {self.date_str}")