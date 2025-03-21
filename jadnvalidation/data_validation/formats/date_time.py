import datetime


class DateTime:
    
    data: str = None
    errors = []    
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        """
        Validates if a string conforms to the RFC 3339 date-time format.
        """
        try:
            # Parse the string using ISO 8601 format (RFC 3339 is a subset of ISO 8601)
            datetime.fromisoformat(self.data.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid date-time format: {self.data}")