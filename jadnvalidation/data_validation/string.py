from jadnvalidation.data_validation.formats.pattern import Pattern
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_fmt_clz_instance
from jadnvalidation.utils.mapping_utils import get_format, get_max_length, get_min_length, get_pattern


common_rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_min_length",
    "}": "check_max_length",
    "%": "check_pattern"
}

json_rules = {}
xml_rules = {}

class String:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Jadn_Type = None
    data: any = None # The string's data only
    data_format: str = None    
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Jadn_Type = None, data: any = None, data_format = JSON):
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
            
    def check_pattern(self):
        pattern = get_pattern(self.j_type)
        if pattern is not None and self.data:
            pattern_instance = Pattern(self.data, pattern)
            pattern_instance.validate()        
        
    def check_type(self):
        if not isinstance(self.data, str):
            self.errors.append(f"Data must be a string. Received: {type(self.data)}")
                        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"String length must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):   
        max_length = get_max_length(self.j_type, self.j_config)
        if len(self.data) > max_length:
            self.errors.append(f"String length must be less than {max_length}. Received: {len(self.data)}")
            
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