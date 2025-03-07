import sys
from typing import Union

# Keep these, used by reflection
from jadnvalidation.data_validation.string import String
from jadnvalidation.data_validation.boolean import Boolean
from jadnvalidation.data_validation.integer import Integer
from jadnvalidation.data_validation.binary import Binary
from jadnvalidation.data_validation.array import Array

from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.utils.general_utils import get_item_safe_check
from jadnvalidation.utils.mapping_utils import convert_to_python_type, get_max_length, get_min_length, is_optional

rules = {
    "type": "check_type",
    "fields": "check_fields",
    "{": "check_minv",
    "}": "check_maxv"
}

class Record:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The record data only
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data  
        
    def check_type(self):
        if not isinstance(self.data, dict):
            self.errors.append(f"Data must be a record / dict. Received: {type(self.data)}")
        
    def check_order(self):
        # TODO: Kevin's logic goes here...
        tbd = ""
        
    def check_minv(self):
        # TODO: Check record props length
        min_length = get_min_length(self.j_type.type_options)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_maxv(self):
        # TODO: Check record props length
        max_length = get_max_length(self.j_type.type_options)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")
        
    def check_fields(self):
        for j_index, j_field in enumerate(self.j_type.fields):
            field_data = get_item_safe_check(self.data, j_index)
            
            if field_data is None:
                if is_optional(j_field[3]):
                    continue
                else:
                    self.errors.append(f"Field '{j_field[1]}' is missing from array data")
                    
            j_field_obj = build_jadn_type_obj(j_field, self.j_type.config)
            p_type = convert_to_python_type(j_field_obj.base_type)
            
            if not isinstance(field_data, p_type):
                self.errors.append(f"Field '{j_field_obj.type_name}' must be of type '{j_field_obj.base_type}'. Received: {type(field_data)})")
                
            # TODO: Remove is_primitive check once compond types are implemented                
            if is_primitive(j_field_obj.base_type):
                p_clz = getattr(sys.modules[__name__], j_field_obj.base_type)
                p_clz = p_clz(j_schema=self.j_schema, j_type=j_field_obj, data=field_data)
                p_clz.validate()      
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True