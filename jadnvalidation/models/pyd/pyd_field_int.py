import datetime
from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import mapping_utils


def build_pyd_int_field(jadn_type: Jadn_Type, force_optional: bool = False) -> Field:
    
    '''
    force_optional: Used by choice fields.
    '''    
    
    pyd_type = mapping_utils.convert_to_pyd_type(jadn_type.base_type)
    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)

    if pyd_field_mapping.is_duration:
        pyd_type = datetime.datetime

    #TODO: We may need a better way to fill in the Field params
    pyd_field = None
    if pyd_field_mapping.is_required and not force_optional:      
        pyd_field = (pyd_type,
                    Field(..., 
                                description=jadn_type.type_description,
                                ge=pyd_field_mapping.ge,
                                le=pyd_field_mapping.le,
                                pattern=pyd_field_mapping.format
                            )
                        )
    else: 
        pyd_field = (pyd_type,
                    Field(default=None, 
                                description=jadn_type.type_description,
                                ge=pyd_field_mapping.ge,
                                le=pyd_field_mapping.le,
                                pattern=pyd_field_mapping.format
                            )
                        )    
  
    return pyd_field