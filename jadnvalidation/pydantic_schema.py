
from pydantic import Field

from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.models.pyd.pyd_field_binary import build_pyd_binary_field
from jadnvalidation.models.pyd.pyd_field_str import build_pyd_str_field
from jadnvalidation.models.pyd.pyd_field_int import build_pyd_int_field
from jadnvalidation.models.pyd.pyd_field_num import build_pyd_num_field
from jadnvalidation.models.pyd.pyd_field_bool import build_pyd_bool_field


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
        #TODO: Add other types      
        case default:
            py_field = build_pyd_binary_field(jadn_type)
        
    return py_field


def build_pyd_fields(jadn_schema: dict) -> dict: 
    pyd_fields = {}  # aka jadn types
    if jadn_schema['types']:
        for type_array in jadn_schema['types']:
            
            jadn_type = Jadn_Type(type_array[0], type_array[1], type_array[2], type_array[3])
            pyd_field = build_pyd_field(jadn_type)
            pyd_fields[jadn_type.type_name] = pyd_field

        return pyd_fields
      
