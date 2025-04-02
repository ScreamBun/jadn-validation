# from email_validator import validate_email, EmailNotValidError
import validators


class Email:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        is_valid = validators.email(self.data)
        if not is_valid:
            raise ValueError(f"'{self.data}' is not a valid email.")
