from typing import Any

from jadnvalidation.models.jadn.jadn_config import Jadn_Config
from jadnvalidation.models.pyd.specializations import Choice
from jadnvalidation.utils.enum_utils import BaseEnum
from jadnvalidation.utils.general_utils import is_field, is_type, safe_get   

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
    CHOICE = 'Choice'
    ENUMERATED = 'Enumerated'
    MAP = 'Map'
    RECORD = 'Record'

class Jadn_Type():
    config: Jadn_Config = Jadn_Config()
    id: str = None
    type_name: str = None
    value: str = None
    base_type: Base_Type = None
    type_options: list[str] = None
    type_description: str = None
    fields: list[Any] = None
    options: Any = None
    required: bool = False
    
    def __init__(self, type_name, base_type, config, id = None, type_options = [], type_description = "", fields = []):
        self.config = config
        self.id = id # available for enums
        self.type_name = type_name
        self.base_type = base_type    
        self.type_options = type_options    
        self.type_description = type_description
        self.fields = fields
        
def is_primitive(jadn_type: Jadn_Type) -> bool:
    if jadn_type in Primitive:
        return True
    else:
        return False
    
def is_enumeration(jadn_type: Jadn_Type) -> bool:
    if jadn_type in Enumeration:
        return True
    else:
        return False 
    
def is_specialization(jadn_type: Jadn_Type) -> bool:
    if jadn_type in Specilization:
        return True
    else:
        return False       
    
def is_structure(jadn_type: Jadn_Type) -> bool:
    if jadn_type in Structure:
        return True
    else:
        return False
    
def build_jadn_type_obj(j_type: list, j_config: Jadn_Config) -> Jadn_Type | None:
    
    jadn_type_obj = None
    
    if is_type(j_type):
        # type
        jadn_type_obj = Jadn_Type(
                config=j_config,
                type_name=j_type[0], 
                base_type=j_type[1], 
                type_options=j_type[2], 
                type_description=j_type[3],
                fields=safe_get(j_type, 4, []))
    elif is_field(j_type):
        # field
        jadn_type_obj = Jadn_Type(
                config=j_config,
                id=j_type[0],
                type_name=j_type[1], 
                base_type=j_type[2], 
                type_options=j_type[3], 
                type_description=j_type[4])     
    else:
        print("unknown jadn item")
    
    return jadn_type_obj