from typing import Union
from jadnvalidation.models.jadn.jadn_field import Jadn_Field
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_j_type
from jadnvalidation.utils.general_utils import get_data_by_name, get_schema_types
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_opts


rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_minv",
    "}": "check_maxv"
}

class Number:
    
    j_schema: dict = {}
    data: int = None
    errors = []   
    
    def __init__(self, j_schema: dict = {}, data: float = None):
        self.j_schema = j_schema
        self.data = data    
        
    def check_format(self, j_obj: Union[Jadn_Type, Jadn_Field], data: float = None):
        # TODO: formats...
        test = ""          
        
    def check_type(self, j_obj: Union[Jadn_Type, Jadn_Field], data: float = None):
        if not isinstance(data, float):
            self.errors.append(ValueError(f"Data must be a float. Received: {type(data)}"))
                        
    def check_minv(self, j_obj: Union[Jadn_Type, Jadn_Field], data: float = None):
        opts = get_opts(j_obj)
        min_length = get_min_length(opts)
        if min_length is not None and len(data) < min_length:
            self.errors.append(ValueError(f"Float length must be greater than or equal to {min_length}. Received: {len(data)}"))
        
    def check_maxv(self, j_obj: Union[Jadn_Type, Jadn_Field], data: float = None):
        opts = get_opts(j_obj)     
        max_length = get_max_length(opts)
        if max_length is not None and len(data) > max_length:
            self.errors.append(ValueError(f"Float length must be less than or equal to {max_length}. Received: {len(data)}"))
            
    def validate(self):
        j_types = self.j_schema.get('types')
        j_float_types = get_schema_types(j_types, Base_Type.NUMBER.value)
        for j_float_type in j_float_types:
            
            j_type_obj = build_j_type(j_float_type)
            int_data = get_data_by_name(self.data, j_type_obj.type_name)
            
            # Check data against rules
            for key, function_name in rules.items():
                getattr(self, function_name)(j_type_obj, int_data)
            
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