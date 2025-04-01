from typing import Union

from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_j_type, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_reference_type, is_even
from jadnvalidation.utils.mapping_utils import get_ktype, get_max_length, get_min_length, get_vtype, is_optional

rules = {
    "type": "check_type",
    "max_elements": "check_max_elements",    
    "{": "check_min_length",
    "}": "check_max_length",
    "key_values": "check_key_values",
}

class MapOf:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The map of data only
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_type(self):
        if isinstance(self.data, list) or isinstance(self.data, dict):
            return
        else:
            raise ValueError(f"Data must be a list / dict / object / record that contains an iterable structure. Received: {type(self.data)}")
        
    def check_max_elements(self):
        if self.data:
            if isinstance(self.data, list):
                if len(self.data) > self.j_config.MaxElements * 2:
                    raise ValueError(f"Data items exceed the maximum limit of {self.j_config.MaxElements}")
                
            if isinstance(self.data, dict):
                if len(self.data) > self.j_config.MaxElements:
                    raise ValueError(f"Data items exceed the maximum limit of {self.j_config.MaxElements}")                
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")

    def validate_type(self, kv_type, data_item):
        if is_primitive(kv_type):
            of_jtype = Jadn_Type("of_" + self.j_type.type_name, kv_type)
            clz_instance = create_clz_instance(kv_type, self.j_schema, of_jtype, data_item)
            clz_instance.validate()
        else:                
            ref_type = get_reference_type(self.j_schema, kv_type)
            ref_type_obj = build_j_type(ref_type)
            clz_instance = create_clz_instance(ref_type_obj.base_type, self.j_schema, ref_type_obj, data_item)
            clz_instance.validate()
        
    def check_key_values(self):
        ktype = get_ktype(self.j_type)
        vtype = get_vtype(self.j_type)
        
        if self.data is None:
            if not is_optional(self.j_type):
                self.errors.append(f"Map of '{self.j_type.type_name}' missing data")
        
        # If ktype is int, then the data is a list of key-value pairs, as follows:
        #  [key1, value1, key2, value2, ...].
        if ktype == Base_Type.INTEGER.value:
            # TODO: Expand this to handle more than just integers?
        
            for i, data_item in enumerate(self.data):
                
                kv_type = None
                if is_even(i):
                    kv_type = ktype
                else:
                    kv_type = vtype
                
                self.validate_type(kv_type, data_item)
                    
        # If ktype is string, then the data is a dict of key-value pairs, as follows:
        #  {"key1": value1, "key2": value2, ...}.
        elif ktype == Base_Type.STRING.value:
            
            for key, val in self.data.items():
                self.validate_type(ktype, key)
                self.validate_type(vtype, val)
                
        else:
            raise ValueError(f"Unknown mapof ktype: {ktype}")
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True
