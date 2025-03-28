from datetime import datetime

from jadnvalidation.utils.consts import TIME_FORMAT


class Time:
    
    time: str = None
    time_format: str = TIME_FORMAT # RFC 3339 Time Format
    
    def __init__(self, time: any = None):
        self.time = time
    
    def validate(self):
        try:
            datetime.strptime(self.time, self.time_format)
        except ValueError:
            raise ValueError(f"Incorrect time format, should be {self.time_format}.  Recieved {self.time}")