import datetime
from ipaddress import IPv4Address, IPv6Address
from pydantic import AnyUrl, EmailStr, Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import custom_annotation, mapping_utils


def build_pyd_dict_field(jadn_type: Jadn_Type) -> Field:
    pyd_type = mapping_utils.convert_to_pyd_type(jadn_type.base_type)
    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)

    # if pyd_field_mapping.is_date:
    #     pyd_type = datetime.date
    
    pyd_field = (pyd_type,
                   Field(..., 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.min_length,
                            max_length=pyd_field_mapping.max_length,
                            pattern=pyd_field_mapping.pattern,
                            
                        )
                )    
    
    return pyd_field