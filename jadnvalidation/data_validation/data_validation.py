import sys

# Keep these, used by reflection
from jadnvalidation.data_validation.array import Array
from jadnvalidation.data_validation.string import String
from jadnvalidation.data_validation.boolean import Boolean
from jadnvalidation.data_validation.integer import Integer

from jadnvalidation.utils.general_utils import get_data_by_name, get_schema_type_by_name


class DataValidation:
    j_schema: dict = {}
    root: str = None
    data: dict = {}
    
    def __init__(self, j_schema: dict, root: str, data: dict):
        self.j_schema = j_schema
        self.root = root
        self.data = data
        
    def validate(self):
        
        try:
            j_types = self.j_schema.get('types')
            root_type = get_schema_type_by_name(j_types, self.root)[0]   
            root_name = root_type[0]
            root_base_type = root_type[1]
            root_data = get_data_by_name(self.data, root_name)
        
            # Reflection
            validation_clz = getattr(sys.modules[__name__], root_base_type)
            validation_clz = validation_clz(j_schema=self.j_schema, j_type=root_type, data=root_data)
            validation_clz.validate()
            
        except Exception as err:           
            raise ValueError(err)