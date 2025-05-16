from datetime import datetime


class Duration:
    
    # Allow different formats?  See date.py
    date_time_str: str = None
    date_time_int: int = None
    date_time_entry: any = None
    
    def __init__(self, date_time_entry: any = None):
        if isinstance(date_time_entry, str):
            self.date_str = date_time_entry
        elif isinstance(date_time_entry, int):
            self.date_time_int = date_time_entry
            self.date_time_str = str(self.date_time_int)
    
    def validate(self):
        if self.date_time_int:
            pass
        elif self.date_time_str:
            try:
                # Parse the string using ISO 8601 format (RFC 3339 is a subset of ISO 8601)
                datetime.fromisoformat(self.date_time_str.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid date-time format: {self.date_time_entry}")
        else: 
                raise ValueError(f"Invalid duration format: {self.date_time_entry}")
        
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