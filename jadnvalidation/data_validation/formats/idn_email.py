from email_validator import validate_email, EmailNotValidError


class IdnEmail:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        try:
            validate_email(self.data, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError((str(e)))
