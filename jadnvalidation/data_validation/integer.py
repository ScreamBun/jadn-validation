from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.mapping_utils import get_format, get_max_length, get_min_length
from jadnvalidation.utils.general_utils import create_fmt_clz_instance


common_rules = {
    "/": "check_format",
    "{": "check_min_val",
    "}": "check_max_val"    
}

json_rules = {
    "type": "json_check_type"
}

xml_rules = {
    "type": "xml_check_type"
}

class Integer:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Union[list, Jadn_Type] = None    
    data: any = None # The int data only
    data_format: str = None
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = [], data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []             
        
    def check_format(self):
        format = get_format(self.j_type)
        if format is not None:
            fmt_clz_instance = create_fmt_clz_instance(format, self.data)
            fmt_clz_instance.validate()        

    def json_check_type(self):
        if self.data is not None:
            format = get_format(self.j_type)
            
            if isinstance(self.data, bool):
                raise ValueError(f"Data for type {self.j_type.type_name} must be of type integer, not Boolean. Received: {type(self.data)}")  
            
            elif isinstance(self.data, int):
                pass
            
            elif isinstance(self.data, str) and format in ['date','date-time','gYear','gMonthDay','gYearMonth', 'yearMonthDuration', 'dayTimeDuration']:
                """ Note: Specific formats may allow users to enter formatted strings in place of integers. 
                    This is their enumeration in this check."""    
                pass
            
            else: 
                raise ValueError(f"Data for type {self.j_type.type_name} must be of type integer. Received: {type(self.data)}")
            
    def xml_check_type(self):
        if self.data is not None:
            format = get_format(self.j_type)
            
            if isinstance(self.data, bool):
                raise ValueError(f"Data for type {self.j_type.type_name} must be of type integer, not Boolean. Received: {type(self.data)}")            
            
            elif isinstance(self.data, int):
                pass
            
            elif isinstance(self.data, str) and format in ['date','date-time','gYear','gMonthDay','gYearMonth']:
                """ Note: Specific formats may allow users to enter formatted strings in place of integers. 
                    This is their enumeration in this check."""    
                pass                  
            
            elif isinstance(self.data, str):
                try:
                    self.data = int(self.data)
                except ValueError as e:
                    raise ValueError(f"Unable to serialize data into an type integer. Received: {type(self.data)}")
            
            else:
                raise ValueError(f"Data for type {self.j_type.type_name} must be of type integer. Received: {type(self.data)}")
                        
    def check_min_val(self):
        min_val = get_min_length(self.j_type)
        if min_val is not None and self.data is None: 
            raise ValueError(f"An Integer value for type {self.j_type.type_name} is required. Received: None")        
        elif min_val is not None and self.data < min_val:
            self.errors.append(f"Integer for type {self.j_type.type_name} must be greater than {min_val}. Received: {len(self.data)}")
        
    def check_max_val(self):
        if self.data is not None: 
            max_val = get_max_length(self.j_type, self.j_config)
            if max_val is not None and self.data > max_val:
                self.errors.append(f"Integer for type {self.j_type.type_name} must be less than {max_val}. Received: {len(self.data)}")           
        
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

