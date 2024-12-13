from enum import Enum
from typing import Any


class Primitive(Enum):
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    
class Structure(Enum):
    ARRAY = 'Array'
    RECORD = 'Record'

class Base_Type(Enum):
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    ARRAY = 'Array'
    RECORD = 'Record'

class Jadn_Type():
    type_name: str = None
    base_type: Base_Type = None
    type_options: list[str] = None
    type_description: str = None
    fields: list[Any] = None
    options: Any = None
    required: bool = False
    
    def __init__(self, type_name, base_type, type_options = [], type_description = "", fields = []):
        self.type_name = type_name
        self.base_type = base_type    
        self.type_options = type_options    
        self.type_description = type_description
        self.fields = fields
        
def is_primitive(jadn_type: Jadn_Type) -> bool:
    if jadn_type in Primitive.__members__:
        return True
    else:
        return False
    
def is_structure(jadn_type: Jadn_Type) -> bool:
    if jadn_type in Structure.__members__:
        return True
    else:
        return False          