from datetime import datetime

from jadnvalidation.utils.consts import TIME_FORMAT


class Time:
    
    time: str = None
    time_format: str = TIME_FORMAT # RFC 3339 Time Format
    
    def __init__(self, time: any = None):
        self.time = time
    
    def validate(self):
        if isinstance(self.time, str):
            try:
                datetime.strptime(self.time, self.time_format)
            except ValueError:
                raise ValueError(f"Incorrect time format, should be {self.time_format}.  Recieved {self.time}")
        elif isinstance(self.time, int):
            try:
                datetime.fromtimestamp(self.time)
            except ValueError:
                raise ValueError(f"Invalid timestamp value: {self.time}")
        else:
            raise ValueError(f"Time must be a string or an integer (timestamp). Received: {type(self.time)}")