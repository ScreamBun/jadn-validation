
from typing import Callable

from pydantic import BaseModel, Field, create_model, field_validator

from models.jadn_type import Jadn_Type
from utils import get_jadn_type_opts


# Pass in minc to determine Optional or not
def convert_type(type_str: str) -> type:
    """
    Converts a jadn type to its corresponding Python type.
    """
    type_mapping = {
        "String": str,
        "Integer": int,
        "Number": float,
        "Boolean": bool,
        "Array": list,
        "Record": dict
        # Add more mappings as needed
        # Binary?
    }
    return type_mapping.get(type_str, str)  # Default to string if type is unknown


def process_properties(properties: dict, property_validators: dict[str, Callable]) -> dict:
    """
    Process the properties of a JSON schema and create Pydantic models for each field.
    """
    processed_properties = {}
    for prop, definition in properties.items():
        prop_type = definition.get("type")
        if prop_type == "object":
            submodel = process_properties(definition["properties"], property_validators)
            processed_properties[prop] = (submodel, ...)
        elif prop_type == "array":
            submodel = process_properties(definition["items"]["properties"], property_validators)
            processed_properties[prop] = [submodel]
        else:
            prop_type = convert_type(prop_type)
            if prop in property_validators:
                processed_properties[prop] = (prop_type, field_validator(prop, mode="after")(property_validators[prop]))
            else:
                processed_properties[prop] = (prop_type, ...)
    return processed_properties


def generate_model(
    schema: dict,
    model_name: str = "DynamicModel",
    property_validators: dict[str, Callable] = {},
) -> type:
    """
    Generate a dynamic Pydantic model from a JADN schema.
    """
    properties = process_properties(schema["properties"], property_validators)
    # Type properties... what about fields??  Maybe hit them if type props work

    return create_model(model_name, **properties)


def dict_model(name: str, dict_def: dict) -> type[BaseModel]:
    fields = {}
    for field_name, value in dict_def.items():
        if isinstance(value, tuple):
            fields[field_name]=value
        elif isinstance(value, dict):
            fields[field_name]=(dict_model(f'{name}_{field_name}', value), ...)
        else:
            raise ValueError(f"Field {field_name}:{value} has invalid syntax")
    return create_model(name, **fields)


# ref: https://docs.pydantic.dev/2.9/concepts/models/#dynamic-model-creation
# ref: https://medium.com/@kevinchwong/dynamic-pydantic-models-for-llamaindex-3b5eb63da980 
def build_pyd_str_field(jadn_type: Jadn_Type) -> Field:
    pyd_data_type = convert_type(jadn_type.base_type)
    
    allowed_type_opts = get_jadn_type_opts(jadn_type.base_type) 
    
    pyd_field = (pyd_data_type,
                   Field(..., 
                        description=jadn_type.type_description,
                        )
                )    
    
    return pyd_field

def build_pyd_int_field(jadn_type: Jadn_Type) -> Field:
    pyd_data_type = convert_type(jadn_type.base_type)
    
    pyd_field = (pyd_data_type,
                   Field(..., 
                        description=jadn_type.type_description,
                        )
                )    
    
    return pyd_field

def build_pyd_num_field(jadn_type: Jadn_Type) -> Field:
    pyd_data_type = convert_type(jadn_type.base_type)
    
    pyd_field = (pyd_data_type,
                   Field(..., 
                        description=jadn_type.type_description,
                        )
                )    
    
    return pyd_field

def build_pyd_bool_field(jadn_type: Jadn_Type) -> Field:
    pyd_data_type = convert_type(jadn_type.base_type)
    
    pyd_field = (pyd_data_type,
                   Field(..., 
                        description=jadn_type.type_description,
                        )
                )    
    
    return pyd_field

#TODO: Add other types

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
        #TODO: Add other types      
        case default:
            py_field = build_pyd_str_field(jadn_type)
        
    return py_field


def build_pyd_fields(jadn_schema: dict) -> dict: 
    pyd_fields = {}  # aka jadn types
    if jadn_schema['types']:
        for type_array in jadn_schema['types']:
            
            jadn_type = Jadn_Type(type_array[0], type_array[1], type_array[2], type_array[3])
            pyd_field = build_pyd_field(jadn_type)
            pyd_fields[jadn_type.type_name] = pyd_field

        return pyd_fields


