import datetime
from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import convert_to_pyd_type, map_type_opts


def build_pyd_str_field(jadn_type: Jadn_Type) -> Field:
    pyd_type = convert_to_pyd_type(jadn_type.base_type)
    
    pyd_field_mapping = map_type_opts(jadn_type.type_options)
    
    if pyd_field_mapping.is_date:
        pyd_type = datetime.datetime
    
    pyd_field = (pyd_type,
                   Field(..., 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.min_length,
                            max_length=pyd_field_mapping.max_length,
                            pattern=pyd_field_mapping.pattern
                        )
                )    
    
    return pyd_field