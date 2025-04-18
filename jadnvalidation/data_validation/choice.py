from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_field_name, check_sys_char, check_type_name, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_j_field, get_reference_type
from jadnvalidation.utils.mapping_utils import get_choice_type, use_field_ids
from jadnvalidation.utils.consts import JSON, XML, Choice_Consts

common_rules = {
    "type": "check_type",
    "choice": "check_choice",
}

json_rules = {}
xml_rules = {}

class Choice:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The choice data only
    data_format: str = None    
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format          
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_type(self):
        if not isinstance(self.data, dict):
            raise ValueError(f"Data must be an object / dictionary. Received: {type(self.data)}")
        
    def process_any_of(self, use_ids):
        
        # At least one field must be present
        num_of_choices = len(self.data)
        num_of_fields = len(self.j_type.fields)
        if num_of_choices > num_of_fields:
            raise ValueError(f"At least one field must be present, but no more {num_of_fields}.  Received: {num_of_choices}.")     
        
        for key, choice_data in self.data.items():
            j_field = get_j_field(self.j_type.fields, key, use_ids)
            
            if j_field is None:
                raise ValueError(f"Choice '{self.j_type.type_name}' key {key} not found. ")
            
            j_field_obj = build_jadn_type_obj(j_field)
            check_sys_char(j_field_obj.type_name, self.j_config.Sys)
            check_field_name(j_field_obj.type_name, self.j_config.FieldName)
        
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                j_field_obj = ref_type_obj
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, choice_data, self.data_format)
            clz_instance.validate()
        
    def process_all_of(self, use_ids):
        
        # TODO: Needs tests more, may be too simple. 
        # All fields must be present
        num_of_choices = len(self.data)
        num_of_fields = len(self.j_type.fields)
        if num_of_choices != num_of_fields:
            raise ValueError(f"Choice '{self.j_type.type_name}' must have exactly {num_of_fields} choices. Received: {num_of_choices}")
        
        for key, choice_data in self.data.items():
            j_field = get_j_field(self.j_type.fields, key, use_ids)
            
            if j_field is None:
                raise ValueError(f"Choice '{self.j_type.type_name}' key {key} not found. ")
            
            j_field_obj = build_jadn_type_obj(j_field)
            check_sys_char(j_field_obj.type_name, self.j_config.Sys)
            check_field_name(j_field_obj.type_name, self.j_config.FieldName)
        
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                j_field_obj = ref_type_obj
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, choice_data, self.data_format)
            clz_instance.validate()
        
    def process_not(self, use_ids):
        for key, choice_data in self.data.items():
            j_field = get_j_field(self.j_type.fields, key, use_ids)
            
            if j_field:
                raise ValueError(f"Choice '{self.j_type.type_name}' key {key} found, but 'not' has been specified.")
        
    def process_one_of(self, use_ids):

        # only one choice is allowed        
        if len(self.data) != 1:
            self.errors.append(f"Choice '{self.j_type.type_name}' must have exactly one choice. Received: {len(self.data)}")
        
        for key, choice_data in self.data.items():
            j_field = get_j_field(self.j_type.fields, key, use_ids)
            
            if j_field is None:
                raise ValueError(f"Choice '{self.j_type.type_name}' key {key} not found. ")
            
            j_field_obj = build_jadn_type_obj(j_field)
            check_sys_char(j_field_obj.type_name, self.j_config.Sys)
            check_field_name(j_field_obj.type_name, self.j_config.FieldName)
        
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                j_field_obj = ref_type_obj
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, choice_data, self.data_format)
            clz_instance.validate()
            
            break # Only one choice is allowed.        
                        
            
    def check_choice(self):
        use_ids = use_field_ids(self.j_type.type_options)
        choice_type = get_choice_type(self.j_type.type_options)
        
        match choice_type:
            case Choice_Consts.CHOICE_ALL_OF:
                self.process_all_of(use_ids)
            case Choice_Consts.CHOICE_ANY_OF:
                self.process_any_of(use_ids)
            case Choice_Consts.CHOICE_NOT:
                self.process_not(use_ids)
            case _:
                self.process_one_of(use_ids)
                                
    def validate(self):
        
        # Check data against rules
        rules = json_rules
        if self.data_format == XML:
            rules = xml_rules
       
       # Data format specific rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
            
        # Common rules across all data formats
        for key, function_name in common_rules.items():
            getattr(self, function_name)()            
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True