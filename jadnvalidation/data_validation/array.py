import sys
from typing import Union

from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_item_safe_check, get_schema_type_by_name
from jadnvalidation.utils.mapping_utils import convert_to_python_type, get_max_length, get_min_length, is_optional

rules = {
    "type": "check_type",
    "order": "check_order",
    "fields": "check_fields",
    "/": "check_format",
    "{": "check_minv",
    "}": "check_maxv"
}

class Array:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The array's data only
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data  
        
    def check_type(self):
        if not isinstance(self.data, list):
            # Note: If the data isn't a list, there's no point to continue with other checks
            # Just raise the error to kill the thread rather than collecting and continuing. 
            raise ValueError(f"Data must be a list. Received: {type(self.data)}")
        
    def check_order(self):
        # TODO: Kevin's logic goes here...
        tbd = ""
        
    def check_minv(self):
        min_length = get_min_length(self.j_type.type_options)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Array length must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_maxv(self):
        max_length = get_max_length(self.j_type.type_options)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Array length must be less than {max_length}. Received: {len(self.data)}")
        
    def check_format(self):
        # TODO: IPV formats...
        tbd = ""
        
    def check_fields(self):
        for j_index, j_field in enumerate(self.j_type.fields):
            field_data = get_item_safe_check(self.data, j_index)
            
            if field_data is None:
                if is_optional(j_field[3]):
                    continue
                else:
                    self.errors.append(f"Field '{j_field[1]}' is missing from array data")
                    
            j_field_obj = build_jadn_type_obj(j_field, self.j_type.config)
            if is_primitive(j_field_obj.base_type):
                p_type = convert_to_python_type(j_field_obj.base_type)
            
                if not isinstance(field_data, p_type):
                    self.errors.append(f"Field '{j_field_obj.type_name}' must be of type '{j_field_obj.base_type}'. Received: {type(field_data)})")
                
                clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, field_data)
                clz_instance.validate()
            else:
                j_types = self.j_schema.get('types')
                ref_type = get_schema_type_by_name(j_types, j_field_obj.base_type)[0]   
                ref_base_type = ref_type[1]
                
                clz_instance = create_clz_instance(ref_base_type, self.j_schema, ref_type, field_data)
                clz_instance.validate()                 
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True