from typing import List, Union
from pydantic import Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import mapping_utils


def build_pyd_list_field(jadn_type: Jadn_Type) -> Field:
    # pyd_type = mapping_utils.convert_to_pyd_type(jadn_type.base_type)
    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)
    field_types = mapping_utils.get_field_types(jadn_type.fields)
    
    pyd_field = (list[Union[tuple(field_types.values())]],
                   Field(..., 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.min_length,
                            max_length=pyd_field_mapping.max_length,
                            pattern=pyd_field_mapping.pattern,
                            
                        )
                )    
    
    return pyd_field