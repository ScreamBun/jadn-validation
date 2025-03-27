from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_opts
from jadnvalidation.utils.general_utils import split_on_first_char


rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_min_val",
    "}": "check_max_val"
}

class Integer:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Union[list, Jadn_Type] = None    
    data: any = None # The int data only
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = []):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        
        self.j_config = get_j_config(self.j_schema)        
        
    def check_format(self):

        val = None
        opts = get_opts(self.j_type)
        for opt in opts:
            opt_key, opt_val = split_on_first_char(opt)
            if "/" == opt_key:

                val = opt_val
                format_min = None
                format_max = None
                format_min = give_format_constraint(val, 0)
                format_max = give_format_constraint(val, 1)
                if self.data > format_max:
                    self.errors.append(f"Data exceeds allowed format length: {format_max}")
                if self.data < format_min:
                    self.errors.append(f"Data does not meet minimum format length: {format_min}")

    def check_type(self):
        if self.data:
            if not isinstance(self.data, int):
                self.errors.append(f"Data must be of type integer. Received: {type(self.data)}")
                        
    def check_min_val(self):
        min_val = get_min_length(self.j_type)
        if min_val is not None and self.data < min_val:
            self.errors.append(f"Integer must be greater than {min_val}. Received: {len(self.data)}")
        
    def check_max_val(self):
        max_val = get_max_length(self.j_type, self.j_config)
        if max_val is not None and self.data > max_val:
            self.errors.append(f"Integer must be less than {max_val}. Received: {len(self.data)}")
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True
                
def give_format_constraint(format: str, option_index: int):

        format_designator, designated_value = split_on_first_char(format) 
        
        if format == 'duration':
            constraint_vals = [0, None]
            return constraint_vals[option_index]

        if format_designator == 'i':            
            try:
                signed_value = int(designated_value) -1
                print("iN value for "+format+" between - and + 2^("+str(designated_value)+"-1)-1")
                unsig_min = pow(-2,signed_value) - 1
                unsig_max = pow(2,signed_value) -1
                struct = [unsig_min, unsig_max]
                return struct[option_index]
            except ValueError as e:
                print("i<n> format requires a numeric component following signed signifier \"i\". \n"+e)
        else: return None
        '''
            if designated_value == '8':
                constraint_vals = [-127, 128]
                return constraint_vals[option_index]
            elif designated_value == '16':
                constraint_vals = [-32768, 32767]
                return constraint_vals[option_index]
            elif designated_value == '32':
                constraint_vals = [-2147483648, 2147483647]
                return constraint_vals[option_index]
        '''
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
