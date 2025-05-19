from datetime import datetime


class Duration:
    
    data: any = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid duration value: {self.data}. Expected an integer / number of seconds.")
        
class DayTimeDuration:
    
    # Allow different formats?  See date.py
    date_time: str = None
    
    def __init__(self, date_time: any = None):
        self.date_time = date_time
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3339 date-time format.
        """
        try:
            # Parse the string using ISO 8601 format (RFC 3339 is a subset of ISO 8601)
            datetime.fromisoformat(self.date_time.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid date-time format: {self.date_time}")
        
class YearMonthDuration:
    
    # Allow different formats?  See date.py
    date_time: str = None
    
    def __init__(self, date_time: any = None):
        self.date_time = date_time
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3339 date-time format.
        """
        try:
            # Parse the string using ISO 8601 format (RFC 3339 is a subset of ISO 8601)
            datetime.fromisoformat(self.date_time.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid date-time format: {self.date_time}")