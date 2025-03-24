from typing import Union
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length

rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_minv",
    "}": "check_maxv"
}

class Binary:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None
    data: any = None # Binary data only
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = []):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data  
        
    def check_type(self):
        if not isinstance(self.data, bytes):
            self.errors.append(f"Data must be binary. Received: {type(self.data)}")
        
    def check_minv(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Binary length must be greater than or equal to {min_length}. Received: {len(self.data)}")
        
    def check_maxv(self):
        max_length = get_max_length(self.j_type)
        if len(self.data) > max_length:
            self.errors.append(f"Binary length must be less than or equal to {max_length}. Received: {len(self.data)}")
        
    def check_format(self):
        # TODO: binary formats...
        tbd = ""
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True