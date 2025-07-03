from datetime import datetime


class DateTime:
    
    # Allow different formats?  See date.py
    date_time: str = None
    
    def __init__(self, date_time: any = None):
        self.date_time = date_time
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3339 date-time format.
        """
        if isinstance(self.date_time, str):
            try:
                # Parse the string using ISO 8601 format (RFC 3339 is a subset of ISO 8601)
                datetime.fromisoformat(self.date_time.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid date-time format: {self.date_time}")
        elif isinstance(self.date_time, int):
            try:
                datetime.fromtimestamp(self.date_time)
            except ValueError:
                raise ValueError(f"Invalid timestamp value: {self.date_time}")
        else:
            raise ValueError(f"Date-time must be a string or an integer (timestamp). Received: {type(self.date_time)}")