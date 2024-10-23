from enum import Enum


class Base_Type(Enum):
    STRING = 'String'
    NUMBER = 'Number'
    INTEGER = 'Integer'
    BOOLEAN = 'Boolean'

class Jadn_Type():
    type_name: str = None
    base_type: Base_Type = None
    type_options: list[str] = None
    type_description: str = None
    # fields: list
    
    def __init__(self, type_name, base_type, type_options, type_description):
        self.type_name = type_name
        self.base_type = base_type    
        self.type_options = type_options    
        self.type_description = type_description    