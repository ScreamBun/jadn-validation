from typing import Union
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_choice_data_content, get_data_by_id, get_data_by_name, get_reference_type
from jadnvalidation.utils.mapping_utils import is_optional, use_field_ids

# id, extend
rules = {
    "type": "check_type",
    "number_of_choices": "check_number_of_choices",
    "choice": "check_choice",
}

class Choice:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The choice data only
    inner_data: any = None # The inner data of the choice
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        
        if self.data:
            self.inner_data = get_choice_data_content(self.data)        
        
    def check_type(self):
        if not isinstance(self.data, dict):
            raise ValueError(f"Data must be an object / dictionary. Received: {type(self.data)}")
            
    def check_number_of_choices(self):
        if self.data is None:
            # if not is_optional(self.j_type.type_options):
            raise ValueError(f"Choice '{self.j_type.type_name}' data is required.")
                
        if self.inner_data is None:
            # if not is_optional(self.j_type.type_options):
            raise ValueError(f"Choice '{self.j_type.type_name}' is required.")
            
        # TODO: Add logic to check for anyOf and allOf. 
        
        # oneOf is the default.
        if len(self.inner_data) != 1:
            self.errors.append(f"Choice '{self.j_type.type_name}' must have exactly one choice. Received: {len(self.inner_data)}")                
                        
            
    def check_choice(self):
        use_ids = use_field_ids(self.j_type.type_options)
        for j_key, j_field in enumerate(self.j_type.fields):
            field_data = None
            if use_ids:
                field_data = get_data_by_id(self.inner_data, j_field[0])
            else:
                field_data = get_data_by_name(self.inner_data, j_field[1])
            
            if field_data is None:
                # if is_optional(j_field[3]):
                continue
            else:
                data_found += 1
                # TODO: Update this to handle anyOf and allOf.
                # raise ValueError(f"Field '{j_field[1]}' is missing from data")
                    
            j_field_obj = build_jadn_type_obj(j_field, self.j_type.config)
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type, self.j_type.config)
                j_field_obj = ref_type_obj
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, field_data)
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