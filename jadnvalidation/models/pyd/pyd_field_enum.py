from typing import Literal
from pydantic import Field
from jadnvalidation.models.jadn.jadn_enum import Jadn_Enum
    

def build_pyd_enum_field(jadn_enum: Jadn_Enum) -> Field:
    pyd_field = (Literal[tuple(jadn_enum.values)],
                    Field(default=None, 
                            validate_assignment=True))
    
    return pyd_field