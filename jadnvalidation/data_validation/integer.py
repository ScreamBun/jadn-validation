from typing import Union
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_opts, map_type_opts
from jadnvalidation.utils.general_utils import split_on_first_char, split_on_second_char


rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_minv",
    "}": "check_maxv"
}

class Integer:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None    
    data: any = None # The int data only
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = []):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data    
        
    def check_format(self):
        # TODO: formats...

        opts = get_opts(self.j_type)
        map_type_opts(self.j_type, opts)        
        min_val = get_min_length(opts)
        if min_val is not None and self.data < min_val:
            self.errors.append(f"Integer must be greater than {min_val}. Received: {len(self.data)}")
        max_val = get_max_length(opts)
        if max_val is not None and self.data > max_val:
            self.errors.append(f"Integer must be less than {max_val}. Received: {len(self.data)}")
        
            #opt_val = self.j_schema[]

    
        
    def check_type(self):
        if self.data:
            if not isinstance(self.data, int):
                self.errors.append(f"Data must be of type integer. Received: {type(self.data)}")
                        
    def check_minv(self):
        opts = get_opts(self.j_type)
        min_val = get_min_length(opts)
        if min_val is not None and self.data < min_val:
            self.errors.append(f"Integer must be greater than {min_val}. Received: {len(self.data)}")
        
    def check_maxv(self):
        opts = get_opts(self.j_type)     
        max_val = get_max_length(opts)
        if max_val is not None and self.data > max_val:
            self.errors.append(f"String length must be less than {max_val}. Received: {len(self.data)}")
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True