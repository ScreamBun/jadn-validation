#from iso8601 import iso8601
#from datetime import datetime    
import re 
        
class GYear:
    
    data: any = None
    
    def __init__(self, data: any = None):
        if isinstance(data, str):
            self.data = data
        elif isinstance(data, int):
            # self.date_int = data
            self.data = str(data)
        else:
            raise ValueError(f"Cannot parse date-time format: {data}")
    
    """#tired of getting grief from this library i'm not sold on anyway.
    def validate(self):

        try:
            # Parse the string using ISO 8601 format
            datetime_converted = iso8601.parse_date(self.date_str)
        except ValueError:
            raise ValueError(f"Invalid date-time format: {self.date_str}")
            """
        
    def validate(self):
        """
        Validates if a string conforms to the RFC 3339 date-time format.
        """
        if self.data is not None:
            try:
                # if re.fullmatch("^-?[0-9]{4}((-[0-9]{2}:[0-9]{2})|Z)?$", self.data, flags=0):
                if re.fullmatch(r"-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?$", self.data, flags=0):
                # if re.fullmatch(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\+|-)((0[0-9]|1[0-3]):([0-5][0-9])|14:00|([0-1][0-9]|2[0-3])([0-5][0-9])|([0-1][0-9]|2[0-3]))?)?$", self.data, flags=0):
                    pass
                else: 
                    raise ValueError(f"Entry does not match gYear: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid gYear: {self.data}")
            
            
            
    # Regex to match gYear format: YYYY or YYYY(+/-)HH:MM or YYYY(+/-)HHMM or YYYY(+/-)HH
    # if re.fullmatch(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\+|-)((0[0-9]|1[0-3]):([0-5][0-9])|14:00|([0-1][0-9]|2[0-3])([0-5][0-9])|([0-1][0-9]|2[0-3]))?)?$", gyear_value):
    #     return True
    # else:
    #     return False            