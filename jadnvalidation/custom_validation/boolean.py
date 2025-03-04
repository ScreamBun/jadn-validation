from typing import Union
from jadnvalidation.models.jadn.jadn_field import Jadn_Field
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_j_type
from jadnvalidation.utils.general_utils import get_data_by_name, get_schema_types
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_opts


rules = {
    "type": "check_type"
}

class Boolean:
    
    j_schema: dict = {}
    data: bool = None
    errors = []   
    
    def __init__(self, j_schema: dict = {}, data: bool = None):
        self.j_schema = j_schema
        self.data = data         
        
    def check_type(self, j_obj: Union[Jadn_Type, Jadn_Field], data: bool = None):
        if not isinstance(data, bool):
            self.errors.append(ValueError(f"Data must be a boolean. Received: {type(data)}"))
            
    def validate(self):
        j_types = self.j_schema.get('types')
        j_str_types = get_schema_types(j_types, Base_Type.BOOLEAN.value)
        for j_str_type in j_str_types:
            
            j_type_obj = build_j_type(j_str_type)
            bool_data = get_data_by_name(self.data, j_type_obj.type_name)
            
            # Check str data against str rules
            for key, function_name in rules.items():
                getattr(self, function_name)(j_type_obj, bool_data)
            
            # Check.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True
    
    def validate_by_j_field(self, j_field_obj: Jadn_Field):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)(j_field_obj, self.data)
        
        # Check.....?
    
        return True