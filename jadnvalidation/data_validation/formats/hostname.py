import validators


class Hostname:
    
    hostname: str = None
    
    def __init__(self, hostname: any = None):
        self.hostname = hostname
    
    def validate(self):
        is_valid = validators.hostname(self.hostname)
        
        if not is_valid:
            raise ValueError(f"'{self.hostname}' is not a valid hostname.")
