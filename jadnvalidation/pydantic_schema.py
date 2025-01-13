
from pydantic import BaseModel, ConfigDict, Field, create_model, validator

from jadnvalidation.consts import DYNAMIC_MODEL
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type
from jadnvalidation.models.pyd.pyd_field_binary import build_pyd_binary_field
from jadnvalidation.models.pyd.pyd_field_str import build_pyd_str_field
from jadnvalidation.models.pyd.pyd_field_int import build_pyd_int_field
from jadnvalidation.models.pyd.pyd_field_num import build_pyd_num_field
from jadnvalidation.models.pyd.pyd_field_record import build_pyd_record_field
from jadnvalidation.models.pyd.pyd_field_bool import build_pyd_bool_field
from jadnvalidation.models.pyd.pyd_model_base import SBBaseModel
from jadnvalidation.models.pyd.structures import Record
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
        case "Record":
            py_field = build_pyd_record_field(jadn_type)            
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

def create_parent_model(child_models: list[BaseModel]):
    fields = {}
    for model in child_models:
        # fields[model.__name__.lower()] = (model, ...)
        fields[model.__name__] = (model, ...)

    return create_model("RootSchema", **fields)

def build_models(j_types: list, j_config = None) -> type[BaseModel]:
    """Creates a Pydantic models dynamically based on a list of JADN Types."""

    p_models = []
    for j_type in j_types:
        j_type_obj = build_jadn_type_obj(j_type)
            
        if j_type_obj:
            
            p_fields = {}
            for j_field in j_type_obj.fields: 
                j_field_obj = build_jadn_type_obj(j_field)
                p_field = build_pyd_field(j_field_obj)
                p_fields[j_field_obj.type_name] = p_field
                
            # TODO: Create add these to build_pyd_field or their own functions
            # TODO: See l_config for global_opts
            p_fields["model_opts"] = (str, Field(default="testing model opts", exclude=True, evaluate=False))
            p_fields["global_opts"] = (str, Field(default="testing global opts", exclude=True, evaluate=False))
    
            p_model = create_model(j_type_obj.type_name, __base__=Record, **p_fields)
            
            p_models.append(p_model)
            
    ParentModel = create_parent_model(p_models)
    
    return ParentModel


# ** MAIN ENTRY POINT **
def create_pyd_model(j_schema: dict) -> type[BaseModel]:
    j_config = j_schema.get('info', {}).get('config')
    j_types = j_schema.get('types')
    custom_model = None
    
    if j_types:
        p_models = build_models(j_types, j_config)
        custom_model = p_models
        # custom_model = create_model('schema', 
        #                             __base__=Record,                                  
        #                             root=(dict, p_models))      
        
        # Try this on Monday
        # https://stackoverflow.com/questions/62267544/generate-pydantic-model-from-a-dict
        # Interesting.. https://jsontopydantic.com/
        # custom_model = create_model(custom_model., Field(..., alias='Record-Name'))
          
    else:
        raise ValueError("Types missing from JADN Schema")
    
    return custom_model

