from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
import base64
from jadnvalidation.utils.general_utils import create_fmt_clz_instance
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_format, get_max_length, get_min_length, get_opts
from jadnvalidation.utils.general_utils import split_on_first_char

rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_min_length",
    "}": "check_max_length"
}

class Binary:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Union[list, Jadn_Type] = None
    data: any = None # Binary data only
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = []):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data  
        self.data_bin = None
        self.data_str = None
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_type(self):
        if isinstance(self.data, bytes):
            try:
                self.data_bytes = self.data
                self.data_string = self.data_bytes.decode('utf-8') # decoding a string for regex and length checks 
            except ValueError as e:
                self.errors.append(f"Error encoding Binary data: "+e)
        elif isinstance(self.data, str):
            try:
                self.data_str = self.data #hi
                self.data_bytes = self.data_str.encode('utf8') # encoding data into bytes from string
            except ValueError as e:
                self.errors.append(f"Error getting binary data from String: "+e)
        else:
            self.errors.append(f"Data must be binary. Received: {type(self.data)}")
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data_str) < min_length:
            self.errors.append(f"Binary length must be greater than or equal to {min_length}. Received: {len(self.data_str)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if len(self.data) > max_length:
            self.errors.append(f"Binary length must be less than or equal to {max_length}. Received: {len(self.data_str)}")
        
    def check_format(self):
        format = get_format(self.j_type)
        if format is not None:
            fmt_clz_instance = create_fmt_clz_instance(format, self.data_str)
            fmt_clz_instance.validate()
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True
