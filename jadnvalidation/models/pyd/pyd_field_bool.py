from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.models.utils import mapping_utils


def build_pyd_bool_field(jadn_type: Jadn_Type) -> Field:
    pyd_data_type = mapping_utils.convert_to_pyd_type(jadn_type.base_type)
    
    pyd_field = (pyd_data_type,
                   Field(..., 
                        description=jadn_type.type_description,
                        )
                )    
    
    return pyd_field