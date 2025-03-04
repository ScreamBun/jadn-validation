import sys
from jadnvalidation.custom_validation.string import String
from jadnvalidation.custom_validation.boolean import Boolean
from jadnvalidation.custom_validation.integer import Integer
from jadnvalidation.models.jadn.jadn_field import build_j_field
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_j_type, is_primitive
from jadnvalidation.utils.general_utils import get_data_by_name, get_item_safe_check, get_schema_types, str_to_class
from jadnvalidation.utils.mapping_utils import convert_to_python_type, get_max_length, get_min_length, is_optional

rules = {
    "type": "check_array_type",
    "order": "check_order",
    "fields": "check_field_types",
    "/": "check_format",
    "{": "check_minv",
    "}": "check_maxv"
}

class Array:
    
    j_schema: dict = {}
    data: dict = {}
    errors = []
    
    def __init__(self, j_schema: dict = {}, data: dict = {}):
        self.j_schema = j_schema
        self.data = data  
        
    def check_array_type(self, j_type_obj: Jadn_Type, data: list = None):
        if not isinstance(data, list):
            self.errors.append(ValueError(f"Data must be a list. Received: {type(data)}"))        
        
    def check_order(self, j_type_obj: Jadn_Type, data: list = None):
        # TODO: Kevin's logic goes here...
        test = ""
        
    def check_minv(self, j_type_obj: Jadn_Type, data: list = None):
        min_length = get_min_length(j_type_obj.type_options)
        if min_length is not None and len(data) < min_length:
            self.errors.append(ValueError(f"Array length must be greater than or equal to {min_length}. Received: {len(data)}"))
        
    def check_maxv(self, j_type_obj: Jadn_Type, data: list = None):
        max_length = get_max_length(j_type_obj.type_options)
        if max_length is not None and len(data) > max_length:
            self.errors.append(ValueError(f"Array length must be less than or equal to {max_length}. Received: {len(data)}"))
        
    def check_format(self, j_type_obj: Jadn_Type, data: list = None):
        # TODO: IPV formats...
        test = ""         
        
    def check_field_types(self, j_type_obj: Jadn_Type, data: list = None):
        for j_index, j_field in enumerate(j_type_obj.fields):
            field_data = get_item_safe_check(data, j_index)
            
            if field_data is None:
                if is_optional(j_field):
                    continue
                else:
                    self.errors.append(ValueError(f"Field '{j_field[1]}' is missing from array data"))
                    
            j_field_obj = build_j_field(j_field)
            p_type = convert_to_python_type(j_field_obj.type)
            
            if not isinstance(field_data, p_type):
                self.errors.append(ValueError(f"Field '{j_field_obj.name}' must be of type '{j_field_obj.type}'. Received: {type(field_data)})"))
                
            if is_primitive(j_field_obj.type):
                p_clz = getattr(sys.modules[__name__], j_field_obj.type)
                p_clz = p_clz(j_schema=self.j_schema, data=field_data)
                p_clz.validate_by_j_field(j_field_obj)      
        
    def validate(self):
        j_types = self.j_schema.get('types') 
        j_array_types = get_schema_types(j_types, Base_Type.ARRAY.value)
        for j_array_type in j_array_types:
            
            j_type_obj = build_j_type(j_array_type, {})
            array_data = get_data_by_name(self.data, j_type_obj.type_name)
            
            # Check array data against array rules
            for key, function_name in rules.items():
                getattr(self, function_name)(j_type_obj, array_data)
                
            # Check field types
            # self.check_field_types(j_type_obj, array_data)
            
            # Check.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True