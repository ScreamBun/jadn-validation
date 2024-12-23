from ipaddress import IPv4Address, IPv6Address
from pydantic import Field
from pydantic_extra_types.mac_address import MacAddress
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.models.utils import mapping_utils


def build_pyd_binary_field(jadn_type: Jadn_Type) -> Field: 
    pyd_type = mapping_utils.convert_to_pyd_type(jadn_type.base_type)
    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)
    
    if pyd_field_mapping.is_eui:
        pyd_type = MacAddress
    if pyd_field_mapping.is_ipv4_addr:
        pyd_type = IPv4Address
    if pyd_field_mapping.is_ipv6_addr:
        pyd_type = IPv6Address           
    
    pyd_field = (pyd_type,
                   Field(..., 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.min_length,
                            max_length=pyd_field_mapping.max_length,
                            pattern=pyd_field_mapping.pattern,
                        )
                )    
    
    return pyd_field 
