from typing import Union

from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_sys_char, check_type_name, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_data_by_name, get_reference_type
from jadnvalidation.utils.mapping_utils import flip_to_array_of, get_max_length, get_max_occurs, get_min_length, get_min_occurs, is_optional

rules = {
    "type": "check_type",
    "{": "check_min_length",
    "}": "check_max_length",
    "fields": "check_fields"
}

class Record:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The record data only
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
        if not isinstance(self.data, dict):
            raise ValueError(f"Data must be a record / dict. Received: {type(self.data)}")
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")
        
    def check_fields(self):
        for j_key, j_field in enumerate(self.j_type.fields):
            field_data = get_data_by_name(self.data, j_field[1])
            j_field_obj = build_jadn_type_obj(j_field)
            
            check_sys_char(j_field_obj.type_name, self.j_config.Sys)
            
            if field_data is None:
                if is_optional(j_field_obj):
                    continue
                else:
                    raise ValueError(f"Field '{j_field[1]}' is missing from data")
            
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                j_field_obj = ref_type_obj
                
            min_occurs = get_min_occurs(j_field_obj)
            max_occurs = get_max_occurs(j_field_obj, self.j_config)
            if min_occurs > 1 or max_occurs > 1:
                j_field_obj = flip_to_array_of(j_field_obj, min_occurs, max_occurs)                
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, field_data)
            clz_instance.validate()
        
    def validate(self):

        # peel out your formats
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True
