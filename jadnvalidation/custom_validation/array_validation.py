from jadnvalidation.models.jadn.jadn_field import build_j_field, convert_j_field_to_j_type
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.pydantic_schema import create_pyd_model 
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
    errors = []
    
    def __init__(self, j_schema: dict = {}, data: dict = {}):
        self.j_schema = j_schema
        self.data = data  
        
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
        
    def check_type(self, j_type_obj: Jadn_Type, data: list = None):
        if not isinstance(data, list):
            self.errors.append(ValueError(f"Data must be a list. Received: {type(data)}"))
        
    def check_field_types(self, j_type_obj: Jadn_Type, data: list = None):
        for j_index, j_field in enumerate(j_type_obj.fields):
            field_data = get_item_safe_check(data, j_index)
            if field_data is None:
                if is_optional(j_field):
                    continue
                else:
                    self.errors.append(ValueError(f"Field '{j_field[1]}' is missing from array data"))
            j_field_obj = build_jadn_type_obj(j_field, {})
            p_type = convert_to_python_type(j_field_obj.base_type)
            if not isinstance(field_data, p_type):
                self.errors.append(ValueError(f"Field '{j_field_obj.type_name}' must be of type '{j_field_obj.base_type}'. Received: {type(field_data)})"))
    
    def check_with_pydantic(self, j_type_obj: Jadn_Type, data: any = None):
        # Left off here... need to:
        # x convert the field into a type
        # x resolve the type if it's not a primitive, run with it if it is a primitive
        # x send the type to pydantic to create a model
        # x use the model to validate the data
        # x capture any errors and store them in a list
        # x if the list is not empty, raise an exception with the list of errors
        
        for j_field_list in j_type_obj.fields:
            j_field_obj = build_j_field(j_field_list, {})
            j_ftype_obj = convert_j_field_to_j_type(j_field_obj)
            
            if is_primitive(j_ftype_obj):
                # TODO: Leftoff here... data type issue... may need to move building logic into smaller callable methods
                pyd_model = create_pyd_model(j_ftype_obj) 
                try :
                    pyd_model.model_validate(data)
                except Exception as err:
                    self.errors.append(ValueError(err))
        
    def validate(self):
        j_types = self.j_schema.get('types')
        j_array_types = get_schema_types(j_types, Base_Type.ARRAY.value)
        for j_array_type in j_array_types:
            
            j_type_obj = build_j_type(j_array_type, {})
            array_data = get_data_by_name(self.data, j_type_obj.type_name)
            
            # Check array data against array rules
            for key, function_name in array_rules.items():
                getattr(self, function_name)(j_type_obj, array_data)
                
            # Check field types
            self.check_field_types(j_type_obj, array_data)
            
            # Use pydantic to validate fields
            self.check_with_pydantic(j_type_obj, array_data)
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True