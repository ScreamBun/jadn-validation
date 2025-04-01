from typing import Union
import base64
import re
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_opts
from jadnvalidation.utils.general_utils import split_on_first_char

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
        self.data_bin = None
        self.data_str = None
        
    def check_type(self):
        if isinstance(self.data, bytes):
            try:
                self.data_bytes = self.data
                self.data_string = self.data.encode('utf-8') # encoding a string for regex and length checks 
            except ValueError as e:
                self.errors.append(f"Error encoding Binary data: "+e)
        elif isinstance(self.data, str):
            try:
                self.data_str = self.data
                self.data_bytes = base64.decodebytes(self.data) # decoding data into bytes from string
            except ValueError as e:
                self.errors.append(f"Error getting binary data from String: "+e)
        else:
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
      format = get_format(self.j_type)
      if format is not None:
          fmt_clz_instance = create_fmt_clz_instance(format, self.data)
          fmt_clz_instance.validate()
    
    
    
    def check_format(self):

        val = None
        opts = get_opts(self.j_type)
        for opt in opts:
            opt_key, opt_val = split_on_first_char(opt)
            if "/" == opt_key:

                val = opt_val
                format_min = None
                format_max = None
                if opt_val == 'eui':
                    if isinstance(self.data, str):
                        match = re.fullmatch("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", self.data, flags=0)
                        if match:
                            pass
                        else:
                            self.errors.append(f"Data does not match EUI: {self.data}")
                    elif isinstance(self.data, Binary):
                        stringy_data = self.data.encode('utf-8')
                        match = re.fullmatch("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", stringy_data, flags=0)
                        if match:
                            pass
                        else:
                            self.errors.append(f"Data does not match EUI: {self.data}")
                elif opt_val == 'ipv4-addr':
                    if isinstance(self.data, str):
                        match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$", self.data, flags=0)
                        if match:
                            pass
                        else:
                            self.errors.append(f"Data does not match ipv4-address: {self.data}")                     
                    elif isinstance(self.data, Binary):
                        stringy_data = self.data.encode('utf-8')
                        match = re.fullmatch("^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$", self.data, flags=0)
                        if match:
                            pass
                        else:
                            self.errors.append(f"Data does not match ipv4-address: {self.data}") 
                elif opt_val == 'ipv6-addr':
                    match = re.fullmatch("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))", self.data, flags=0)
                    if match:
                        pass
                    else:
                        self.errors.append(f"Data does not match ipv6-address: {self.data}") 
                if format_max:
                    if self.data > format_max:
                        self.errors.append(f"Data exceeds allowed format length: {format_max}")
                if format_min:
                    if self.data < format_min:
                        self.errors.append(f"Data does not meet minimum format length: {format_min}")
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True
    
    def create_fmt_clz_instance(class_name: str, *args, **kwargs):
    
    modules = {
        "Date" : "jadnvalidation.data_validation.formats.date",
        "DateTime" : "jadnvalidation.data_validation.formats.date_time",
        "Time" : "jadnvalidation.data_validation.formats.time"
    }