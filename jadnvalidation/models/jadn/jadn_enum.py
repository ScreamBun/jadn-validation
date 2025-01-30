from typing import Union
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type
from jadnvalidation.utils.general_utils import safe_get

def allowed_values_check(values: Union[int, str] = []):
    if len(set(map(type, values))) != 1:
        raise ValueError("Enum cannot contain mixed types.")     

class Jadn_Enum():
    name: str = None
    base_type = Base_Type.ENUMERATED.value
    enum_type = str
    values: Union[int, str] = []
    
    def __init__(self, name: str, enum_type, values: Union[int, str] = []):
        self.name = name
        self.enum_type = enum_type
        self.values = values
        
def build_jadn_enum_field_obj(j_type_obj: Jadn_Type, use_id: bool = False) -> Jadn_Enum | None:
    enum_field_obj = {}
    allowed_values = []
    enum_type = str
    
    if use_id:
        enum_type = int
    
    for field in j_type_obj.fields:
        field_id = safe_get(field, 0, None)
        field_name = safe_get(field, 1, None)
        if use_id:
            allowed_values.append(field_id)
        else:
            allowed_values.append(field_name)
    
    allowed_values_check(allowed_values)
    
    enum_field_obj = Jadn_Enum(
            name=j_type_obj.type_name,
            enum_type=enum_type,
            values=allowed_values)
    
    return enum_field_obj       
