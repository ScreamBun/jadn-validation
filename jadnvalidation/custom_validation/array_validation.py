from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_jadn_type_obj
from jadnvalidation.utils.general_utils import get_data_by_name, get_item_safe_check, get_schema_types
from jadnvalidation.utils.mapping_utils import convert_to_python_type, get_max_length, get_min_length, is_optional

array_rules = {
    "type": "check_type",
    "order": "check_order",
    "/": "check_format",
    "{": "check_minv",
    "}": "check_maxv"
}

class ArrayValidation:
    
    j_schema: dict = {}
    data: dict = {}
    
    def __init__(self, j_schema: dict = {}, data: dict = {}):
        self.j_schema = j_schema
        self.data = data  
        
    def check_order(self, j_type_obj: Jadn_Type, data: list = None):
        # TODO: Kevin's logic goes here...
        test = ""
        
    def check_minv(self, j_type_obj: Jadn_Type, data: list = None):
        min_length = get_min_length(j_type_obj.type_options)
        if min_length is not None and len(data) < min_length:
            raise ValueError(f"Array length must be greater than or equal to {min_length}. Received: {len(data)}")
        
    def check_maxv(self, j_type_obj: Jadn_Type, data: list = None):
        max_length = get_max_length(j_type_obj.type_options)
        if max_length is not None and len(data) > max_length:
            raise ValueError(f"Array length must be less than or equal to {max_length}. Received: {len(data)}")
        
    def check_format(self, j_type_obj: Jadn_Type, data: list = None):
        # TODO: IPV formats...
        test = ""         
        
    def check_type(self, j_type_obj: Jadn_Type, data: list = None):
        if not isinstance(data, list):
            raise ValueError(f"Data must be a list. Received: {type(data)}")
        
    def check_field_types(self, j_type_obj: Jadn_Type, data: list = None):
        for j_index, j_field in enumerate(j_type_obj.fields):
            field_data = get_item_safe_check(data, j_index)
            if field_data is None:
                if is_optional(j_field):
                    continue
                else:
                    raise ValueError(f"Field '{j_field[1]}' is missing from array data")
            j_field_obj = build_jadn_type_obj(j_field, {})
            p_type = convert_to_python_type(j_field_obj.base_type)
            if not isinstance(field_data, p_type):
                raise ValueError(f"Field '{j_field_obj.type_name}' must be of type '{j_field_obj.base_type}'. Received: {type(field_data)})") 
        
    def validate(self):
        j_types = self.j_schema.get('types')
        schema_arrays = get_schema_types(j_types, Base_Type.ARRAY.value)
        for array in schema_arrays:
            j_type_obj = build_jadn_type_obj(array, {})
            array_data = get_data_by_name(self.data, j_type_obj.type_name)
            
            # Check array data against array rules
            for key, function_name in array_rules.items():
                getattr(self, function_name)(j_type_obj, array_data)
                
            # Check field types
            self.check_field_types(j_type_obj, array_data)