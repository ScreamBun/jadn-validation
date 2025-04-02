import re

class Eui:
    
    data_str: str = ""
    data: bytes = None
    errors = []    
    
    def __init__(self, data: any = None):
        if isinstance(self.data, str):
            self.data_str = data
        else:   
            self.data_str = self.data.decode('utf-8')
    
    def validate(self):
        """
        Validates if a string matches an EUI with either hyphens or colons.
        """
        try:
            match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$", self.data_str, flags=0)
            if match:
                pass
            else:
                self.errors.append(f"Data does not match eui: {self.data_str}")
        except Exception as err:
            raise ValueError(err)