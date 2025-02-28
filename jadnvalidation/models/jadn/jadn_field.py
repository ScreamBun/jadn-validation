from jadnvalidation.models.jadn.jadn_config import Jadn_Config
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type
from jadnvalidation.utils.general_utils import is_field

class Jadn_Field():
    config: Jadn_Config = Jadn_Config()
    id: str = None
    name: str = None
    type: Base_Type = None
    options: list[str] = None
    description: str = None
    
    def __init__(self, name, type, id = None, config = None, options = None, description = None):
        self.config = config
        self.id = id # available for enums
        self.name = name
        self.type = type    
        self.options = options    
        self.description = description

def build_j_field(j_type: list, j_config: Jadn_Config) -> Jadn_Field | None:
    j_field = None
    if is_field(j_type):
        j_field = Jadn_Field(
                config=j_config,
                id=j_type[0],
                name=j_type[1], 
                type=j_type[2], 
                options=j_type[3], 
                description=j_type[4])
    else:
        print("unknown jadn item")        
    return j_field

def convert_j_field_to_j_type(j_field: Jadn_Field) -> Jadn_Type | None:
    j_type = Jadn_Type(
            config=j_field.config,
            id=j_field.id,
            type_name=j_field.name,
            base_type=j_field.type, 
            type_options=j_field.options, 
            type_description=j_field.description,
            fields=[])
    return j_type