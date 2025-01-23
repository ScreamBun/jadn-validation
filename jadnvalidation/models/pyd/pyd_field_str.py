import datetime
from ipaddress import IPv4Address, IPv6Address
from pydantic import AnyUrl, EmailStr, Field
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils import custom_annotation, mapping_utils


def build_pyd_str_field(jadn_type: Jadn_Type) -> Field:
    pyd_type = mapping_utils.convert_to_pyd_type(jadn_type.base_type)
    pyd_field_mapping = mapping_utils.map_type_opts(jadn_type.base_type, jadn_type.type_options)

    if pyd_field_mapping.is_date:
        pyd_type = datetime.date
    
    elif pyd_field_mapping.is_datetime:
        pyd_type = datetime.datetime
        
    elif pyd_field_mapping.is_time:
        pyd_type = datetime.time        
        
    elif pyd_field_mapping.is_email:
        pyd_type = EmailStr
        
    elif pyd_field_mapping.is_idn_email:
        # Note: email-validation handles internationilzation out-of-the-box
        pyd_type = EmailStr
        
    elif pyd_field_mapping.is_hostname: 
        pyd_type = custom_annotation.Hostname
        
    elif pyd_field_mapping.is_idn_hostname:
        pyd_type = custom_annotation.IdnHostname
        
    elif pyd_field_mapping.is_ipv4:
        pyd_type = IPv4Address
        
    elif pyd_field_mapping.is_ipv6:
        pyd_type = IPv6Address               
        
    elif pyd_field_mapping.is_iri:
        pyd_type = AnyUrl
        
    elif pyd_field_mapping.is_iri_ref:
        pyd_type = AnyUrl
        
    elif pyd_field_mapping.is_json_pointer:
        pyd_type = custom_annotation.PydJsonPointer   
        
    elif pyd_field_mapping.is_relative_json_pointer:
        pyd_type = custom_annotation.PydRelJsonPointer            
      
    elif pyd_field_mapping.is_regex:
        pyd_type = custom_annotation.PydRegex      
        
    elif pyd_field_mapping.is_uri:
        pyd_type = AnyUrl      
        
    elif pyd_field_mapping.is_uri_ref:
        # note: pypi rfc3986 could be used here if AnyUrl is too broad
        # https://pypi.org/project/rfc3986/ 
        pyd_type = AnyUrl
        
    elif pyd_field_mapping.is_uri_template:
        pyd_type = custom_annotation.UriTemplate
        
    if pyd_field_mapping.max_length == None:
        pyd_field_mapping.max_length = jadn_type.config.MaxString
    
    #TODO: Need optional vs required logic, at the moment everything is required ...
    pyd_field = (pyd_type,
                   Field(..., 
                            description=jadn_type.type_description,
                            min_length=pyd_field_mapping.min_length,
                            max_length=pyd_field_mapping.max_length,
                            pattern=pyd_field_mapping.pattern, 
                            # strict=True,
                            validate_assignment=True
                        )
                )    
    
    return pyd_field