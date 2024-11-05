from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.models.utils import mapping_utils


def build_pyd_num_field(jadn_type: Jadn_Type) -> Field:
    pyd_type = mapping_utils.convert_to_pyd_type(jadn_type.base_type)

    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)
    
    pyd_field = (pyd_type,
                   Field(..., 
                            description=jadn_type.type_description,
                            ge=pyd_field_mapping.ge,
                            le=pyd_field_mapping.le,
                            pattern=pyd_field_mapping.format
                        )
                )    
    
    return pyd_field