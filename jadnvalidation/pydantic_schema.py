
from __future__ import annotations
import re
from typing import Union
from pydantic import BaseModel, Field, create_model

from jadnvalidation.models.jadn.jadn_config import GLOBAL_CONFIG_KEY, ROOT_GLOBAL_CONFIG_KEY, TYPE_OPTS_KEY, Jadn_Config, build_jadn_config_obj
from jadnvalidation.models.jadn.jadn_enum import Jadn_Enum, build_jadn_enum_field_obj
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_jadn_type_obj, is_enumeration, is_primitive, is_specialization, is_structure
from jadnvalidation.models.pyd.pyd_field_array import build_pyd_array_field
from jadnvalidation.models.pyd.pyd_field_binary import build_pyd_binary_field
from jadnvalidation.models.pyd.pyd_field_choice import build_pyd_choice_field
from jadnvalidation.models.pyd.pyd_field_enum import build_pyd_enum_field
from jadnvalidation.models.pyd.pyd_field_ref import build_pyd_ref_field
from jadnvalidation.models.pyd.pyd_field_str import build_pyd_str_field
from jadnvalidation.models.pyd.pyd_field_int import build_pyd_int_field
from jadnvalidation.models.pyd.pyd_field_num import build_pyd_num_field
from jadnvalidation.models.pyd.pyd_field_record import build_pyd_record_field
from jadnvalidation.models.pyd.pyd_field_bool import build_pyd_bool_field
from jadnvalidation.models.pyd.specializations import Choice
from jadnvalidation.models.pyd.structures import Map, Record
from jadnvalidation.utils import mapping_utils


def build_pyd_field(jadn_type: Union[Jadn_Type, Jadn_Enum], force_optional: bool = False) -> Field:
    py_field = ()
    match jadn_type.base_type:
        case Base_Type.STRING.value:
            py_field = build_pyd_str_field(jadn_type, force_optional)
        case Base_Type.INTEGER.value:
            py_field = build_pyd_int_field(jadn_type, force_optional)
        case Base_Type.NUMBER.value:
            py_field = build_pyd_num_field(jadn_type, force_optional)
        case Base_Type.BOOLEAN.value:
            py_field = build_pyd_bool_field(jadn_type, force_optional) 
        case Base_Type.BINARY.value:
            py_field = build_pyd_binary_field(jadn_type, force_optional)
        case Base_Type.ENUMERATED.value:
            py_field = build_pyd_enum_field(jadn_type) 
        case Base_Type.CHOICE.value:
            py_field = build_pyd_choice_field(jadn_type, force_optional)          
        case Base_Type.RECORD.value:
            py_field = build_pyd_record_field(jadn_type, force_optional) 
        case "Array":
            py_field = build_pyd_array_field(jadn_type, force_optional)
        case default:
            # Custom Type (aka ref type)
            py_field = build_pyd_ref_field(jadn_type, force_optional)
        
    return py_field

def create_root_model(sub_models: dict[str, BaseModel], root_fields: dict[str, Field]):
    
    fields = {}
    for model_name, model in sub_models.items():
        # TODO: Sys name?
        fields[model.__name__] = (model, ...)


    for field_name, field in root_fields.items():
        # TODO: Sys name?
        fields[field_name] = field

    return create_model("root_model", __base__=Record, **fields)

def validate_type_name(name: str, j_config: Jadn_Config):
    
    if name.startswith(j_config.Sys):
        raise ValueError(f"Type Name {name} cannot begin with {j_config.Sys}")
    
    if not re.search(j_config.TypeName, name):
        raise ValueError(f"Invalid Type Name {name} per the Schema / info / config / $TypeName regex")
    
def validate_field_name(name: str, j_config: Jadn_Config):
    
    if name.startswith(j_config.Sys):
        raise ValueError(f"Field {name} cannot begin with {j_config.Sys}")
    
    if not re.search(j_config.FieldName, name):
        raise ValueError(f"Invalid Field Name {name} per the Schema / info / config / $FieldName regex")

def build_custom_model(j_types: list, j_config_data = {}) -> type[BaseModel]:
    """Creates a Pydantic model dynamically based on a list of JADN Types and JADN Configurations."""

    j_config_obj = build_jadn_config_obj(j_config_data)

    p_models = {}
    p_fields = {}
    for j_type in j_types:
        j_type_obj = build_jadn_type_obj(j_type, j_config_obj)
        validate_type_name(j_type_obj.type_name, j_config_obj)
            
        if j_type_obj:

            if is_enumeration(j_type_obj.base_type):
                use_id = mapping_utils.use_enum_id(j_type_obj.type_options)
                j_field_obj = build_jadn_enum_field_obj(j_type_obj, use_id)
                p_field = build_pyd_field(j_field_obj)
                p_fields[j_type_obj.type_name] = p_field
                
            # TODO: Possibly combine with is_structure block of code below....                
            elif is_specialization(j_type_obj.base_type):                
                p_structure_fields = {}
                for j_field in j_type_obj.fields: 
                    j_field_obj = build_jadn_type_obj(j_field, j_config_obj)
                    validate_field_name(j_field_obj.type_name, j_config_obj)
                    p_field = build_pyd_field(j_field_obj, True)
                    p_structure_fields[j_field_obj.type_name] = p_field
                    
                j_type_opts_obj = None
                if j_type_obj.type_options:
                   j_type_opts_obj = mapping_utils.map_type_opts(j_type_obj.base_type, j_type_obj.type_options)                    
                    
                p_structure_fields[TYPE_OPTS_KEY] = (str, Field(default=j_type_opts_obj, exclude=True, evaluate=False))
                p_structure_fields[GLOBAL_CONFIG_KEY] = (dict, Field(default=j_config_obj, exclude=True, evaluate=False))                    
                    
                p_models[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Choice, **p_structure_fields)
                globals()[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Choice, **p_structure_fields)

            elif is_structure(j_type_obj.base_type):
                p_structure_fields = {}
                for j_field in j_type_obj.fields: 
                    j_field_obj = build_jadn_type_obj(j_field, j_config_obj)
                    validate_field_name(j_field_obj.type_name, j_config_obj)
                    p_field = build_pyd_field(j_field_obj)
                    p_structure_fields[j_field_obj.type_name] = p_field
                
                j_type_opts_obj = None
                if j_type_obj.type_options:
                   j_type_opts_obj = mapping_utils.map_type_opts(j_type_obj.base_type, j_type_obj.type_options)                
                
                if j_type_obj.base_type == Base_Type.RECORD.value:
                    p_structure_fields[TYPE_OPTS_KEY] = (dict, Field(default=j_type_opts_obj, exclude=True, evaluate=False))
                    p_structure_fields[GLOBAL_CONFIG_KEY] = (dict, Field(default=j_config_obj, exclude=True, evaluate=False))
                                    
                    p_models[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Record, **p_structure_fields)
                    globals()[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Record, **p_structure_fields)
                elif j_type_obj.base_type == Base_Type.MAP.value:
                    p_structure_fields[TYPE_OPTS_KEY] = (dict, Field(default=j_type_opts_obj, exclude=True, evaluate=False))
                    p_structure_fields[GLOBAL_CONFIG_KEY] = (dict, Field(default=j_config_obj, exclude=True, evaluate=False))
                                    
                    p_models[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Map, **p_structure_fields)
                    globals()[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Map, **p_structure_fields)                    
                else:
                    raise ValueError("Unknown JADN Structure")                    
                    
            elif is_primitive(j_type_obj.base_type):
                p_field = build_pyd_field(j_type_obj)
                p_fields[j_type_obj.type_name] = p_field
            else:
                # TODO: Add other bases types...
                raise ValueError("Unknown JADN Type")
            
    # p_fields[ROOT_TYPE_OPTS_KEY] = (str, Field(default="testing root model opts", exclude=True, evaluate=False))
    p_fields[ROOT_GLOBAL_CONFIG_KEY] = (dict, Field(default=j_config_obj, exclude=True, evaluate=False))             
            
    root_model = create_root_model(p_models, p_fields)
    root_model.model_rebuild(_parent_namespace_depth=3, raise_errors=True)
    
    return root_model



# ** MAIN ENTRY POINT **
def create_pyd_model(j_schema: dict) -> type[BaseModel]:
    j_config = j_schema.get('info', {}).get('config')
    j_types = j_schema.get('types')
    custom_model = None
    
    if j_types:
        custom_model = build_custom_model(j_types, j_config)
    else:
        raise ValueError("Types missing from JADN Schema")
    
    return custom_model

def data_validation(model, data):
    try :
        model.model_validate(data)
    except Exception as err:
        raise ValueError(err)

