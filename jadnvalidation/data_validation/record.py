from typing import Union

from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_data_by_name, get_reference_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, is_optional

rules = {
    "type": "check_type",
    "{": "check_minv",
    "}": "check_maxv",
    "fields": "check_fields"
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
            # Note: If the data isn't a list, there's no point to continue with other checks
            # Just raise the error to kill the thread rather than collecting and continuing. 
            raise ValueError(f"Data must be a record / dict. Received: {type(self.data)}")
        
    def check_order(self):
        # TODO: Kevin's logic goes here...
        tbd = ""
        
    def check_minv(self):
        min_length = get_min_length(self.j_type.type_options)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_maxv(self):
        # TODO: Add logic to verify the # of data fields does not exceed the # of schema fields
        max_length = get_max_length(self.j_type.type_options)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")
        
    def check_fields(self):
        for j_key, j_field in enumerate(self.j_type.fields):
            field_data = get_data_by_name(self.data, j_field[1])
            
            if field_data is None:
                if is_optional(j_field[3]):
                    continue
                else:
                    raise ValueError(f"Field '{j_field[1]}' is missing from array data")

            j_field_obj = build_jadn_type_obj(j_field, self.j_type.config)
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type, self.j_type.config)
                j_field_obj = ref_type_obj
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, field_data)
            clz_instance.validate()
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True
