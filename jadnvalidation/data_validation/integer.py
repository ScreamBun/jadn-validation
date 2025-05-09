from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.mapping_utils import get_format, get_max_length, get_min_length, get_opts
from jadnvalidation.utils.general_utils import split_on_first_char, create_fmt_clz_instance


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
        
    def give_format_constraint(self, format: str, option_index: int):
            format_designator, designated_value = split_on_first_char(format) 
            
            if format == 'duration':
                constraint_vals = [0, None]
                
                return constraint_vals[option_index]

            elif format_designator == 'i':            
                try:
                    signed_value = int(designated_value) -1
                    unsig_min = pow(-2,signed_value) - 1
                    unsig_max = pow(2,signed_value) -1
                    struct = [unsig_min, unsig_max]
                    
                    return struct[option_index]
                except ValueError as e:
                    raise ValueError(f"i<n> format requires a numeric component following signed signifier. {e}")

            elif format_designator == "u":
                try:
                    unsigned_value = int(designated_value)
                    unsig_min = 0
                    unsig_max = pow(2,unsigned_value)
                    struct = [unsig_min, unsig_max]
                    
                    return struct[option_index]
                except ValueError as e:
                    raise ValueError(f"u<n> format requires a numeric component following unsigned signifier. {e}")
            else: 
                return None         
        
    def check_format(self):
        # val = None
        
        format = get_format(self.j_type)
        if format is not None:
            fmt_clz_instance = create_fmt_clz_instance(format, self.data)
            fmt_clz_instance.validate()        
          
        # opts = get_opts(self.j_type)
        # for opt in opts:
        #     opt_key, opt_val = split_on_first_char(opt)
            
        #     if "/" == opt_key:
        #         if opt_val in ["date", "data-time", "gYear", "gMonthDay", "gYearMonth"]:
        #             """Set aside formats with bizzarre entry possibilities, regex checks, or odd logic that is 
        #             outside the usual size or value constraint paradigm for integer formats. 
        #             Think Dates; LogicalIntegers the user may attempt to represent with... 
        #             let us be charitable and say UNIQUE formatting applied to them"""
        #             cls = create_fmt_clz_instance(opt_val, self.data)
        #             cls.validate()
        #             break
        #         else:

        #             val = opt_val
        #             format_min: int = None
        #             format_max: int = None
        #             format_min = self.give_format_constraint(val, 0)
        #             format_max = self.give_format_constraint(val, 1)
        #             if self.data > format_max:
        #                 self.errors.append(f"Data exceeds allowed format length: {format_max}")
        #             if self.data < format_min:
        #                 self.errors.append(f"Data does not meet minimum format length: {format_min}")
        #         val = opt_val
        #         format_min = None
        #         format_max = None
        #         format_min = self.give_format_constraint(val, 0)
        #         format_max = self.give_format_constraint(val, 1)
                
        #         if self.data > format_max:
        #             self.errors.append(f"Data for type {self.j_type} exceeds allowed format length: {format_max}")
                    
        #         if self.data < format_min:
        #             self.errors.append(f"Data for type {self.j_type} does not meet minimum format length: {format_min}")

    def json_check_type(self):
        if self.data is not None:
            
            format = get_format(self.j_type)
                  
            # TODO: Boolean check needed, True = 1, False = 0 in python
            if not isinstance(self.data, int):
                # opts = get_opts(self.j_type)                
                if isinstance(self.data, bool):
                    raise ValueError(f"Data for type {self.j_type.type_name} must be of type integer, not Boolean. Received: {type(self.data)}")  
                elif format in ['date','date-time','gYear','gMonthDay','gYearMonth']:   
                    """Specific formats may allow users to enter formatted strings in place of integers. this is their enumeration in this check."""
                    if not isinstance(self.data, str):
                        raise ValueError(f"Data for type {self.j_type.type_name} not a parseable type. Received: {type(self.data)}")

                else: 
                    raise ValueError(f"Data for type {self.j_type.type_name} must be of type integer. Received: {type(self.data)}")
                
            else:
                pass
            
    def xml_check_type(self):
        if self.data is not None:
            if isinstance(self.data, str):
                try:
                    self.data = int(self.data)
                except ValueError as e:
                    raise ValueError(f"Unable to serialize data into an type integer. Received: {type(self.data)}")
            
            if not isinstance(self.data, int):
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

