from typing import Union
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_opts, get_format_max, get_format_min, get_format


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

            # opts = get_opts(self.j_type)
            # format = get_format(self.j_schema)       
            # min_val = get_min_length(opts)
            # format_min = get_format_min(format)
            # if format_min > min_val:
            #     min_val = format_min
            # if min_val is not None and self.data < min_val:
            #     self.errors.append(f"Integer must be greater than {min_val}. Received: {len(self.data)}")
            # max_val = get_max_length(opts)
            # format_max = get_format_max(format)
            # if format_max > min_val:
            #     min_val = format_max
            # if max_val is not None and self.data > max_val:
            #     self.errors.append(f"Integer must be less than {max_val}. Received: {len(self.data)}")
        pass
        

    def check_type(self):
        if self.data:
            if not isinstance(self.data, int):
                self.errors.append(f"Data must be of type integer. Received: {type(self.data)}")
                        
    def check_minv(self):
        min_val = get_min_length(self.j_type)
        if min_val is not None and self.data < min_val:
            self.errors.append(f"Integer must be greater than {min_val}. Received: {len(self.data)}")
        
    def check_maxv(self):
        max_val = get_max_length(self.j_type)
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