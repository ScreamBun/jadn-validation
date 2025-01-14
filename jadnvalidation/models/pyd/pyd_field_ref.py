from __future__ import annotations
from typing import Annotated, ForwardRef

from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils.general_utils import str_to_class


def build_pyd_ref_field(jadn_type: Jadn_Type) -> Field: 
    # pyd_type = jadn_type.type_name
    pyd_type = jadn_type.base_type
    # ref_name = "RootSchema." + pyd_type 
    # pyd_type = "jadnvalidation.pydantic_schema.RecordName2"
    # pyd_type = str_to_class(jadn_type.base_type)
    
    #TODO: determine ref field opts
    # pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)          
    
    # pyd_field_old = (pyd_type,
    #                Field(
    #                         default=None,
    #                         description=jadn_type.type_description,
    #                         title="reference type"
    #                         # min_length=pyd_field_mapping.min_length,
    #                         # max_length=pyd_field_mapping.max_length
    #                     )
    #             )
    
    pyd_field = Annotated[pyd_type, Field(default=pyd_type)]
    # pyd_field = ForwardRef(pyd_type)
    
    return pyd_field 