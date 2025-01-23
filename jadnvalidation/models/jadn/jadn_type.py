from enum import Enum, EnumMeta
from typing import Any

from jadnvalidation.models.jadn.jadn_config import Jadn_Config

# TODO: Move to utils
class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True
    
# TODO: Move to utils
class BaseEnum(Enum, metaclass=MetaEnum):
    pass    

class Primitive(BaseEnum):  
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    
class Structure(BaseEnum):
    ARRAY = 'Array'
    RECORD = 'Record'

class Base_Type(BaseEnum):
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    ARRAY = 'Array'
    RECORD = 'Record'

class Jadn_Type():
    config: Jadn_Config = Jadn_Config()
    type_name: str = None
    base_type: Base_Type = None
    type_options: list[str] = None
    type_description: str = None
    fields: list[Any] = None
    options: Any = None
    required: bool = False
    
    def __init__(self, type_name, base_type, config, type_options = [], type_description = "", fields = []):
        self.config = config
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
    
def is_structure(jadn_type: Jadn_Type) -> bool:
    if jadn_type in Structure:
        return True
    else:
        return False          