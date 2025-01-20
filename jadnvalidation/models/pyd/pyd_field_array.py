from __future__ import annotations
from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import mapping_utils


def build_pyd_array_field(jadn_type: Jadn_Type) -> Field: 
    pyd_type = jadn_type.type_name
    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)          
    
    pyd_field = (pyd_type,
                   Field(   
                            default=None, 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.min_length,
                            max_length=pyd_field_mapping.max_length
                        )
                )    
    
    return pyd_field 