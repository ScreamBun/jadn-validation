from typing import Any

from jadnvalidation.utils.enum_utils import BaseEnum
from jadnvalidation.utils.general_utils import is_enumerated, is_field, is_type, safe_get

class Primitive(BaseEnum):  
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    
class Enumeration(BaseEnum):
    ENUMERATED = 'Enumerated'
    
class Specilization(BaseEnum):
    CHOICE = 'Choice'
    
class Structure(BaseEnum):
    ARRAY = 'Array'
    MAP = 'Map'
    RECORD = 'Record'

class Base_Type(BaseEnum):
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    ARRAY = 'Array'
    ARRAY_OF = 'ArrayOf'
    CHOICE = 'Choice'
    ENUMERATED = 'Enumerated'
    MAP = 'Map'
    MAP_OF = 'MapOf'
    RECORD = 'Record'

class Jadn_Type():
    id: str = None
    type_name: str = None
    value: str = None
    base_type: Base_Type = None
    type_options: list[str] = None
    type_description: str = None
    fields: list[Any] = None
    required: bool = False
    
    def __init__(self, type_name, base_type, id = None, type_options = [], type_description = "", fields = []):
        self.id = id # available for enums
        self.type_name = type_name
        self.base_type = base_type    
        self.type_options = type_options    
        self.type_description = type_description
        self.fields = fields
        
def is_primitive(type: str) -> bool:
    if type in Primitive:
        return True
    else:
        return False
    
def is_enumeration(jadn_type: Jadn_Type) -> bool:
    if jadn_type.base_type in Enumeration:
        return True
    else:
        return False 
    
def is_specialization(jadn_type: Jadn_Type) -> bool:
    if jadn_type.base_type in Specilization:
        return True
    else:
        return False       
    
def is_structure(jadn_type: Jadn_Type) -> bool:
    if jadn_type.base_type in Structure:
        return True
    else:
        return False
    
def is_array(jadn_type: Jadn_Type) -> bool:
    if jadn_type.base_type == Base_Type.ARRAY.value:
        return True
    else:
        return False      
    
def is_record_or_map(jadn_type: Jadn_Type) -> bool:
    if jadn_type.base_type == Base_Type.RECORD.value or jadn_type.base_type == Base_Type.MAP.value:
        return True
    else:
        return False    
    
# Careful, this one combines types and fields
def build_jadn_type_obj(j_type: list) -> Jadn_Type | None:
    jadn_type_obj = None

    if is_enumerated(j_type):
        jadn_type_obj = Jadn_Type(
                id=j_type[0],
                type_name=j_type[1], 
                base_type=None, 
                type_options=[], 
                type_description=j_type[2])
    elif is_type(j_type):
        jadn_type_obj = Jadn_Type(
                type_name=j_type[0], 
                base_type=j_type[1], 
                type_options=j_type[2], 
                type_description=j_type[3],
                fields=safe_get(j_type, 4, []))
    elif is_field(j_type):
        jadn_type_obj = Jadn_Type(
                id=j_type[0],
                type_name=j_type[1], 
                base_type=j_type[2], 
                type_options=j_type[3], 
                type_description=j_type[4])

    else:
        print("unknown jadn item")
    
    return jadn_type_obj

def build_j_type(j_type: list) -> Jadn_Type | None:
    jadn_type_obj = None
    
    if is_type(j_type):
        jadn_type_obj = Jadn_Type(
                type_name=j_type[0], 
                base_type=j_type[1], 
                type_options=j_type[2], 
                type_description=j_type[3],
                fields=safe_get(j_type, 4, []))   
    else:
        raise ValueError("Invalid jadn type")
    
    return jadn_type_obj