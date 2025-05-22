class SignedInteger:
    
    data: any = None
    bits: int = None


    def __init__(self, data: any = None, bits: int = None):
        self.data = data
        self.bits = bits
    
    def validate(self):

        try:
            signed_value = int(self.bits) -1
            print("iN value for "+format+" between - and + 2^("+str(self.bits)+"-1)-1")
            unsig_min = pow(-2,signed_value) - 1
            if self.data < unsig_min:
                self.errors.append(" value less than format minimum")
            unsig_max = pow(2,signed_value) -1
            if self.data < unsig_max:
                self.errors.append("value greater than format maximum")
        except ValueError as e:
            print("i<n> format requires a numeric component following signed signifier \"i\". \n"+e)

"""

def give_format_constraint(format: str, option_index: int):

        format_designator, designated_value = split_on_first_char(format) 


        if format_designator == "u":
            try:
                unsigned_value = int(designated_value)
                print("uN value is 2^"+str(unsigned_value))
                unsig_min = 0
                unsig_max = pow(2,unsigned_value)
                struct = [unsig_min, unsig_max]
                return struct[option_index]
            except ValueError as e:
                print("u<n> format requires a numeric component following unsigned signifier \"u\". \n"+e)
        else: return None
        """