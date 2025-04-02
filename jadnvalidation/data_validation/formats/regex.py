from jadnvalidation.utils.general_utils import create_regex

class Regex:
    reg_pattern = None
    
    def __init__(self, reg_pattern: any = None):
        self.reg_pattern = reg_pattern
    
    def validate(self):
            try:  
                create_regex(self.reg_pattern)
            except ValueError:
                raise ValueError(f"Invalid ECMAScript Regex: {self.reg_pattern}")
            