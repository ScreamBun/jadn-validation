from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type


rules = {
    "type": "check_type"
}

class Boolean:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The boolean's data only
    errors = [] 
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = []):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []         
        
    def check_type(self):
        if isinstance(self.j_type, str):
            if (self.j_type.lower() in ['true', '1', 'y', 'yes']):
                self.data = True
            if (self.j_type.lower() in ['false', '0', 'n', 'no']):
                self.data = False
        
        if not isinstance(self.data, bool):
            self.errors.append(f"Data must be a boolean. Received: {type(self.data)}")
    
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True