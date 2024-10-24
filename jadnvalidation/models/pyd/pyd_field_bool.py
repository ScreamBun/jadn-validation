from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import convert_to_pyd_type


def build_pyd_bool_field(jadn_type: Jadn_Type) -> Field:
    pyd_data_type = convert_to_pyd_type(jadn_type.base_type)
    
    pyd_field = (pyd_data_type,
                   Field(..., 
                        description=jadn_type.type_description,
                        )
                )    
    
    return pyd_field