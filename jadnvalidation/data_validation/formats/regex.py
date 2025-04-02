import re

class Regex:
    data = None
    errors = []    
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
            try: 
                match = re.match(self.data, "", flags=0) 
                '''attempts to match with given regex string. if match or not, it can build; if error in attempt, not regex.'''

            except ValueError:
                self.errors.append('Invalid ECMAScript Regex: '+self.data)
            