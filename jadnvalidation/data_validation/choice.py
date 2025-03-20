from typing import Union
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_j_field, get_reference_type
from jadnvalidation.utils.mapping_utils import use_field_ids

# id, extend
rules = {
    "type": "check_type",
    "multiplicity": "check_multiplicity",
    "choice": "check_choice",
}

class Choice:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The choice data only
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data      
        
    def check_type(self):
        if not isinstance(self.data, dict):
            raise ValueError(f"Data must be an object / dictionary. Received: {type(self.data)}")
            
    def check_multiplicity(self):
        if self.data is None:
            # if not is_optional(self.j_type.type_options):
            raise ValueError(f"Choice '{self.j_type.type_name}' data is required.")
            
        # TODO: Add logic to check for anyOf and allOf. 
        
        # oneOf is the default.
        if len(self.data) != 1:
            self.errors.append(f"Choice '{self.j_type.type_name}' must have exactly one choice. Received: {len(self.data)}")                
                        
            
    def check_choice(self):
        use_ids = use_field_ids(self.j_type.type_options)
        
        for key, choice_data in self.data.items():
            j_field = get_j_field(self.j_type.fields, key, use_ids)
            
            if j_field is None:
                raise ValueError(f"Choice '{self.j_type.type_name}' key {key} not found. ")
            
            j_field_obj = build_jadn_type_obj(j_field, self.j_type.config)
        
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type, self.j_type.config)
                j_field_obj = ref_type_obj
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, choice_data)
            clz_instance.validate()
            
            break # Only one choice is allowed. 
            # TODO: Update this to handle anyOf and allOf.
            
    def check_extra_fields(self):
        # TODO: Check if data has fields that are not specified in the schema
        test = ""
                                
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True