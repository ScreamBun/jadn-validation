from __future__ import annotations
from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import mapping_utils


def build_pyd_choice_field(jadn_type: Jadn_Type, force_optional: bool = False) -> Field: 
    
    '''
    force_optional: Used by choice fields.
    '''    
    
    pyd_type = jadn_type.type_name
    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)          
    
    #TODO: We may need a better way to fill in the Field params
    pyd_field = None
    if pyd_field_mapping.is_required and not force_optional:      
        pyd_field = (pyd_type,
                    Field(..., 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.min_length,
                            max_length=pyd_field_mapping.max_length
                        )
                    )
    else: 
        pyd_field = (pyd_type,
                    Field(default=None, 
                                description=jadn_type.type_description,
                                min_length=pyd_field_mapping.min_length,
                                max_length=pyd_field_mapping.max_length
                            )
                    )        
    
    return pyd_field