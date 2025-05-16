from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_fmt_clz_instance
from jadnvalidation.utils.mapping_utils import get_format, get_max_exclusive, get_max_inclusive, get_min_exclusive, get_min_inclusive


common_rules = {
    "w": "check_min_inclusive",
    "x": "check_max_inclusive",
    "y": "check_min_exclusive",
    "z": "check_max_exclusive",
    "/": "check_format"
}

json_rules = {
    "type": "json_check_type"
}

xml_rules = {
    "type": "xml_check_type"
}

class Number:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Union[list, Jadn_Type] = None
    data: float = None # The number data only
    data_format: str = None
    errors: list = []
    continue_checks: bool = True
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = [], data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format        
        
        self.j_config = get_j_config(self.j_schema) 
        self.errors = []
        self.continue_checks = True
        
    def check_format(self):
        if self.data is not None:
            format = get_format(self.j_type)
            if format is not None:
                fmt_clz_instance = create_fmt_clz_instance(format, self.j_schema, self.j_type, self.data, self.data_format)
                fmt_clz_instance.validate()
                self.continue_checks = False 
        
    def json_check_type(self):
        if self.data is not None:   
            if not isinstance(self.data, float):
                self.errors.append(f"Data must be a float. Received: {type(self.data)}")        
        
    def xml_check_type(self):
        if self.data is not None:
            if isinstance(self.data, str):
                try:
                    self.data = float(self.data)
                except ValueError as e:
                    raise ValueError(f"Unable to serialize data into an type float. Received: {type(self.data)}")
                        
        if not isinstance(self.data, float):
            self.errors.append(f"Data must be a float. Received: {type(self.data)}")
            
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
        rules = json_rules
        if self.data_format == XML:
            rules = xml_rules
       
       # Data format specific rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
            
        # Common rules across all data formats
        for key, function_name in common_rules.items():
            getattr(self, function_name)()            
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True