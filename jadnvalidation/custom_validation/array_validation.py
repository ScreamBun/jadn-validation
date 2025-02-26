from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_jadn_type_obj
from jadnvalidation.utils.general_utils import get_data_by_name, get_schema_types

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
        # TODO: Leftoff here, need function to get minv from jadn_type_obj
        test = ""
        
    def check_maxv(self, j_type_obj: Jadn_Type, data: list = None):
        test = ""
        
    def check_format(self, j_type_obj: Jadn_Type, data: list = None):
        # TODO: IPV formats...
        test = ""         
        
    def check_type(self, j_type_obj: Jadn_Type, data: list = None):
        if not isinstance(data, list):
            raise ValueError(f"Data must be a list. Received: {type(data)}")
        
    def validate(self):
        j_types = self.j_schema.get('types')
        schema_arrays = get_schema_types(j_types, Base_Type.ARRAY.value)
        for array in schema_arrays:
            j_type_obj = build_jadn_type_obj(array, {})
            array_data = get_data_by_name(self.data, j_type_obj.type_name)
            for key, function_name in array_rules.items():
                getattr(self, function_name)(j_type_obj, array_data)