from typing import Union

import numpy as np
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML


common_rules = {
    "type": "check_type",
    "check": "check_floating_point"
}

json_rules = {}

xml_rules = {}

class F16:
    """
    F16 class for validating and converting 16-bit floating-point numbers.
    """
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Jadn_Type = None
    data: any = None
    data_format: str = None
    errors = []      

    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format        
        
        self.j_config = get_j_config(self.j_schema) 
        self.errors = []
        
    def check_type(self):
        if self.data is not None:   
            if not isinstance(self.data, float):
                raise ValueError(f"Data for Type {self.j_type.type_name} must be a float/number. Received: {type(self.data)}")
                
    def check_floating_point(self):
        """Checks if a float is within the range of an f16 (approximate)."""
        
        if self.data is not None:
            
            if np.isinf(self.data) or np.isnan(self.data):
                raise ValueError(f"Data {self.data} for Type {self.j_type.type_name} is not a valid 16-bit float representation.")            
                     
            # Approximate limits for f16
            # Move to consts if needed outside of this class
            F16_MIN = -65504.0
            F16_MAX = 65504.0
            
            if F16_MIN <= self.data <= F16_MAX:
                pass
            else:
                raise ValueError(f"Data {self.data} for Type {self.j_type.type_name} is out of range for 16-bit float representation.")
    
    def validate(self) -> bool:
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
        
