from __future__ import annotations
import re
from typing import Annotated, ForwardRef

from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils.general_utils import str_to_class


ValidName = re.compile(r"^[A-Za-z_][A-Za-z0-9_]_")
SysAlias = re.compile(r"[:$?&|!{}\[\]()^~*\"'+\-\s]")

def clsName(name: str) -> str:
    if ValidName.match(name):
        return name
    return SysAlias.sub("__", name)

def build_pyd_ref_field(jadn_type: Jadn_Type) -> Field: 
    # pyd_type = jadn_type.type_name
    pyd_type = clsName(jadn_type.base_type)
    is_required = True
    # ref_name = "RootSchema." + pyd_type 
    # pyd_type = "jadnvalidation.pydantic_schema.RecordName2"
    # pyd_type = str_to_class(jadn_type.base_type)
    
    #TODO: determine ref field opts
    # pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)          
    
    if is_required:
        pyd_field = (pyd_type,
                   Field(
                            ...,
                            description=jadn_type.type_description,
                            title="reference type",
                            # min_length=pyd_field_mapping.min_length,
                            # max_length=pyd_field_mapping.max_length
                        )
                )
    else:
        pyd_field = (pyd_type,
                   Field(
                            default=None,
                            description=jadn_type.type_description,
                            title="reference type"
                            # min_length=pyd_field_mapping.min_length,
                            # max_length=pyd_field_mapping.max_length
                        )
                )        
        
    
    # pyd_field = Annotated[pyd_type, Field(default=pyd_type)]
    
    return pyd_field 