from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML


common_rules = {
 "type": "check_type"    
}

json_rules = {}
xml_rules = {}

class Boolean:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The boolean's data only
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
            
            if isinstance(self.data, str):
                if (self.data.lower() in ['true', '1', 'y', 'yes']):
                    self.data = True
                elif (self.data.lower() in ['false', '0', 'n', 'no']):
                    self.data = False
                elif "" == self.data:
                    self.data = False
                elif self.data:
                    self.data = True
                
            elif isinstance(self.data, int):
                if 0 == self.data:
                    self.data = False
                elif 1 == self.data:
                    self.data = True
                    
            else:
                raise ValueError(f"Data must be a boolean, string or integer. Received: {type(self.data)}")
            
            if not isinstance(self.data, bool):
                raise ValueError(f"Data must be a boolean. Received: {type(self.data)}")
    
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