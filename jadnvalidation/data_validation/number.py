from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_max_exclusive, get_max_inclusive, get_min_exclusive, get_min_inclusive


rules = {
    "type": "check_type",
    "/": "check_format",
    # "{": "check_min_length",
    # "}": "check_max_length",
    "w": "check_min_inclusive",
    "x": "check_max_inclusive",
    "y": "check_min_exclusive",
    "z": "check_max_exclusive",
}

class Number:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Union[list, Jadn_Type] = None    
    data: float = None # The number data only
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = []):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        
        self.j_config = get_j_config(self.j_schema) 
        self.errors = []   
        
    def check_format(self):
        # TODO: formats...
        tbd = ""          
        
    def check_type(self):
        if not isinstance(self.data, float):
            self.errors.append(f"Data must be a float. Received: {type(self.data)}")
                        
    # def check_min_length(self):
    #     min_length = get_min_length(self.j_type)
    #     if min_length is not None and self.data < min_length:
    #         self.errors.append(f"String length must be greater than or equal to {min_length}. Received: {len(self.data)}")
        
    # def check_max_length(self): 
    #     max_length = get_max_length(self.j_type, self.j_config)
    #     if max_length is not None and self.data > max_length:
    #         self.errors.append(f"String length must be less than or equal to {max_length}. Received: {len(self.data)}")
            
    # Instance is greater than or equal to option value        
    def check_min_inclusive(self): 
        min_inclusive_val = get_min_inclusive(self.j_type)
        if min_inclusive_val is not None and self.data < min_inclusive_val: 
            self.errors.append(f"Number must be greater than or equal to {min_inclusive_val}. Received: {len(self.data)}")            
    
    # Instance is less than or equal to option value
    def check_max_inclusive(self): 
        max_inclusive_val = get_max_inclusive(self.j_type)
        if max_inclusive_val is not None and self.data > max_inclusive_val: 
            self.errors.append(f"Number must be less than or equal to {max_inclusive_val}. Received: {len(self.data)}")
    
    # Instance is greater than option value
    def check_min_exclusive(self): 
        min_exclusive_val = get_min_exclusive(self.j_type)
        if min_exclusive_val is not None and self.data <= min_exclusive_val: 
            self.errors.append(f"Number must be greater than {min_exclusive_val}. Received: {len(self.data)}")
    
    # Instance is less than option value
    def check_max_exclusive(self): 
        max_exclusive_val = get_max_exclusive(self.j_type)
        if max_exclusive_val is not None and self.data >= max_exclusive_val: 
            self.errors.append(f"Number must be less than {max_exclusive_val}. Received: {len(self.data)}")
           
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True