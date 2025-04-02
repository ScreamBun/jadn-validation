import re

class Eui:
    
    data_str: str = None
    data_bin: bytes = None
    errors = []    
    
    def __init__(self, data: any = None):
        self.data_str = data
    
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
        except ValueError:
            raise ValueError(f"Invalid eui format: {self.data_str}")