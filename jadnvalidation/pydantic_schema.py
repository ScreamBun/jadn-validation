
from pydantic import BaseModel, Field, create_model, field_validator, validator

from jadnvalidation.consts import DYNAMIC_MODEL
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type
from jadnvalidation.models.pyd.pyd_field_binary import build_pyd_binary_field
from jadnvalidation.models.pyd.pyd_field_str import build_pyd_str_field
from jadnvalidation.models.pyd.pyd_field_int import build_pyd_int_field
from jadnvalidation.models.pyd.pyd_field_num import build_pyd_num_field
from jadnvalidation.models.pyd.pyd_field_bool import build_pyd_bool_field
from jadnvalidation.models.pyd.pyd_model_base import SBBaseModel
from jadnvalidation.utils import mapping_utils
from jadnvalidation.utils.general_utils import is_field, is_type, safe_get


'''
Refs: 
https://docs.pydantic.dev/2.9/concepts/models/#dynamic-model-creation
https://medium.com/@kevinchwong/dynamic-pydantic-models-for-llamaindex-3b5eb63da980
'''

def build_pyd_field(jadn_type: Jadn_Type) -> Field:
    py_field = ()
    match jadn_type.base_type:
        case "String":
            py_field = build_pyd_str_field(jadn_type)
        case "Integer":
            py_field = build_pyd_int_field(jadn_type)
        case "Number":
            py_field = build_pyd_num_field(jadn_type)
        case "Boolean":
            py_field = build_pyd_bool_field(jadn_type) 
        case "Binary":
            py_field = build_pyd_binary_field(jadn_type)             
        #TODO: Add other types, record recursion needed... 
        case default:
            py_field = build_pyd_str_field(jadn_type)
        
    return py_field

def build_jadn_type_obj(j_type: list) -> Jadn_Type | None:
    
    jadn_type_obj = None
    
    if is_type(j_type):
        # type
        jadn_type_obj = Jadn_Type(
                type_name=j_type[0], 
                base_type=j_type[1], 
                type_options=j_type[2], 
                type_description=j_type[3],
                fields=safe_get(j_type, 4, []))
    elif is_field(j_type):
        # field
        jadn_type_obj = Jadn_Type(
                type_name=j_type[1], 
                base_type=j_type[2], 
                type_options=j_type[3], 
                type_description=j_type[4])     
    else:
        print("unknown jadn item")    
    
    return jadn_type_obj

def add_record_validations(model, jadn_type_obj):

    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type_obj.base_type, jadn_type_obj.type_options)
    if pyd_field_mapping and pyd_field_mapping.min_length:
        model.minv = Field(default=pyd_field_mapping.min_length)

    if pyd_field_mapping and pyd_field_mapping.max_length:
        model.maxv = Field(default=pyd_field_mapping.max_length)
        
    model.jadn_type = jadn_type_obj.base_type
    
    return model

def process_fields(j_types: list, j_config = None) -> type[BaseModel]:
    """Creates a Pydantic model dynamically from a nested dictionary schema."""

    fields = {}
    for j_type in j_types:
        jadn_type_obj = build_jadn_type_obj(j_type)
            
        if jadn_type_obj:
            
            if jadn_type_obj.base_type == Base_Type.RECORD.value:
                # If the field is a nested dictionary, recursively create a nested model
                submodel = process_fields(jadn_type_obj.fields, j_config)
                fields[jadn_type_obj.type_name] = (submodel, ...)
            
            # TODO: Add other structures here...
            
            else:
                # Otherwise, use the field type directly
                pyd_field = build_pyd_field(jadn_type_obj)
                fields[jadn_type_obj.type_name] = pyd_field
                
    # return create_model(DYNAMIC_MODEL, __base__=SBBaseModel, **fields)
    return fields

def build_pyd_model_old(j_types: list, j_config = None) -> type[BaseModel]:
    """Creates a Pydantic model dynamically from a nested dictionary schema."""

    fields = {}
    sb_base_model = SBBaseModel()

    for j_type in j_types:
        jadn_type_obj = build_jadn_type_obj(j_type) 

        if jadn_type_obj:
            
            # If the field is a dictionary then recursively create a new inner model
            if jadn_type_obj.base_type == Base_Type.RECORD.value:
                
                # get type opts...drop in base model for storage and model validation
                pyd_field_mapping = mapping_utils.map_type_opts(jadn_type_obj.base_type, jadn_type_obj.type_options)
                if pyd_field_mapping and pyd_field_mapping.min_length:
                    sb_base_model.minv = pyd_field_mapping.min_length

                if pyd_field_mapping and pyd_field_mapping.max_length:
                    sb_base_model.maxv = pyd_field_mapping.max_length
                
                inner_model = process_fields(jadn_type_obj.fields, j_config)
                fields[jadn_type_obj.type_name] = (inner_model, ...)
            
            # TODO: Add other structures here...
            
            else:
                # Otherwise, use the field type directly
                pyd_field = build_pyd_field(jadn_type_obj)
                fields[jadn_type_obj.type_name] = pyd_field
        
    return create_model('DynamicModel', __base__=sb_base_model, **fields)

# ** MAIN ENTRY POINT **
def create_pyd_model(j_schema: dict) -> type[BaseModel]:
    j_config = j_schema.get('info', {}).get('config')
    j_types = j_schema.get('types')
    custom_model = None
    
    if j_types:
        fields = process_fields(j_types, j_config)
        custom_model = create_model('root', **fields)        
    else:
        raise ValueError("Types missing from JADN Schema")
    
    return custom_model

