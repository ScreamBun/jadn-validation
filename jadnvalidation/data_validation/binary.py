from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_opts
from jadnvalidation.utils.general_utils import split_on_first_char

rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_min_length",
    "}": "check_max_length"
}

class Binary:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Union[list, Jadn_Type] = None
    data: any = None # Binary data only
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = []):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data  
        
        self.j_config = get_j_config(self.j_schema)
        
    def check_type(self):
        if not isinstance(self.data, bytes):
            self.errors.append(f"Data must be binary. Received: {type(self.data)}")
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Binary length must be greater than or equal to {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if len(self.data) > max_length:
            self.errors.append(f"Binary length must be less than or equal to {max_length}. Received: {len(self.data)}")
        
    def check_format(self):

        val = None
        opts = get_opts(self.j_type)
        for opt in opts:
            opt_key, opt_val = split_on_first_char(opt)
            if "/" == opt_key:

                val = opt_val
                format_min = None
                format_max = None
                if opt_val == 'eui':
                    pass
                elif opt_val == 'ipv4-addr':
                    pass
                elif opt_val == 'ipv6-addr':
                    pass
                if self.data > format_max:
                    self.errors.append(f"Data exceeds allowed format length: {format_max}")
                if self.data < format_min:
                    self.errors.append(f"Data does not meet minimum format length: {format_min}")
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True