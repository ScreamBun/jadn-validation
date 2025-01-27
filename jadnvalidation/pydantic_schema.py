
from __future__ import annotations
from pydantic import BaseModel, Field, create_model

from jadnvalidation.models.jadn.jadn_config import Jadn_Config, build_jadn_config_obj
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_jadn_type_obj, is_primitive, is_structure
from jadnvalidation.models.pyd.pyd_field_array import build_pyd_array_field
from jadnvalidation.models.pyd.pyd_field_binary import build_pyd_binary_field
from jadnvalidation.models.pyd.pyd_field_ref import build_pyd_ref_field
from jadnvalidation.models.pyd.pyd_field_str import build_pyd_str_field
from jadnvalidation.models.pyd.pyd_field_int import build_pyd_int_field
from jadnvalidation.models.pyd.pyd_field_num import build_pyd_num_field
from jadnvalidation.models.pyd.pyd_field_record import build_pyd_record_field
from jadnvalidation.models.pyd.pyd_field_bool import build_pyd_bool_field
from jadnvalidation.models.pyd.structures import Record
from jadnvalidation.utils import mapping_utils


def build_pyd_field(jadn_type: Jadn_Type) -> Field:
    py_field = ()
    match jadn_type.base_type:
        case Base_Type.STRING.value:
            py_field = build_pyd_str_field(jadn_type)
        case Base_Type.INTEGER.value:
            py_field = build_pyd_int_field(jadn_type)
        case Base_Type.NUMBER.value:
            py_field = build_pyd_num_field(jadn_type)
        case Base_Type.BOOLEAN.value:
            py_field = build_pyd_bool_field(jadn_type) 
        case Base_Type.BINARY.value:
            py_field = build_pyd_binary_field(jadn_type)
        case "Record":
            py_field = build_pyd_record_field(jadn_type) 
        case "Array":
            py_field = build_pyd_array_field(jadn_type)                
        case default:
            # Custom Type (aka ref type)
            py_field = build_pyd_ref_field(jadn_type)
        
    return py_field

# Still used??
def add_record_validations(model, jadn_type_obj):

    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type_obj.base_type, jadn_type_obj.type_options)
    if pyd_field_mapping and pyd_field_mapping.min_length:
        model.minv = Field(default=pyd_field_mapping.min_length)

    if pyd_field_mapping and pyd_field_mapping.max_length:
        model.maxv = Field(default=pyd_field_mapping.max_length)
        
    model.jadn_type = jadn_type_obj.base_type
    
    return model

def create_root_model(sub_models: dict[str, BaseModel], root_fields: dict[str, Field]):
    
    fields = {}
    for model_name, model in sub_models.items():
        # TODO: Sys name?
        fields[model.__name__] = (model, ...)


    for field_name, field in root_fields.items():
        # TODO: Sys name?
        fields[field_name] = field

    return create_model("root_model", __base__=Record, **fields)

def validate_name(name: str, j_config: Jadn_Config):
    
    if name.startswith(j_config.Sys):
        raise ValueError(f"{name} cannot begin with {j_config.Sys}")

def build_custom_model(j_types: list, j_config_data = {}) -> type[BaseModel]:
    """Creates a Pydantic model dynamically based on a list of JADN Types and JADN Configurations."""

    j_config_obj = build_jadn_config_obj(j_config_data)

    p_structure_models = {}
    p_primitive_fields = {}
    for j_type in j_types:
        j_type_obj = build_jadn_type_obj(j_type, j_config_obj)
        validate_name(j_type_obj.type_name, j_config_obj)
            
        if j_type_obj:

            p_structure_fields = {}
            if is_structure(j_type_obj.base_type):
                for j_field in j_type_obj.fields: 
                    j_field_obj = build_jadn_type_obj(j_field, j_config_obj)
                    validate_name(j_field_obj.type_name, j_config_obj)
                    p_field = build_pyd_field(j_field_obj)
                    p_structure_fields[j_field_obj.type_name] = p_field
                    
                # TODO: Need different bases per type... 
                p_structure_models[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Record, **p_structure_fields)
                globals()[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Record, **p_structure_fields)                    
                
                # TODO: Create add these to build_pyd_field or their own functions
                # TODO: See l_config for global_opts
                p_structure_fields["type_opts"] = (str, Field(default="testing model opts", exclude=True, evaluate=False))
                p_structure_fields["global_opts"] = (dict, Field(default=j_config_obj, exclude=True, evaluate=False))                
                    
            elif is_primitive(j_type_obj.base_type):
                p_field = build_pyd_field(j_type_obj)
                p_primitive_fields[j_type_obj.type_name] = p_field
            else:
                raise ValueError("Unknown JADN Type")
            
    p_primitive_fields["root_type_opts"] = (str, Field(default="testing root model opts", exclude=True, evaluate=False))
    p_primitive_fields["root_global_opts"] = (dict, Field(default=j_config_obj, exclude=True, evaluate=False))             
            
    root_model = create_root_model(p_structure_models, p_primitive_fields)

    try :
        root_model.model_rebuild(
            _parent_namespace_depth=3,
            raise_errors=True
            )
    except Exception as err:
        print(err)
    
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

