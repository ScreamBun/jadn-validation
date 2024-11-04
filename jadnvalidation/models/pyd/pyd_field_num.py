from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import convert_to_pyd_type, map_type_opts



def build_pyd_num_field(jadn_type: Jadn_Type) -> Field:
    pyd_data_type = convert_to_pyd_type(jadn_type.base_type)

    pyd_field_mapping = map_type_opts(jadn_type.type_options)
    
    pyd_field = (pyd_data_type,
                   Field(..., 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.ge,
                            max_length=pyd_field_mapping.le,
                            pattern=pyd_field_mapping.format
                        )
                )    
    
    return pyd_field