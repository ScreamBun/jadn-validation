class Pyd_Field_Mapper():
    min_length: int = None 
    max_length: int = None
    ge: int = None
    le: int = None
    is_date: bool = False
    is_datetime: bool = False
    is_email: bool = False
    is_idn_email: bool = False
    is_eui: bool = False
    is_time: bool = False
    is_hostname: bool = False
    is_idn_hostname: bool = False
    is_ipv4: bool = False
    is_ipv4_addr: bool = False
    is_ipv6: bool = False
    is_ipv6_addr: bool = False
    is_iri: bool = False
    is_iri_ref: bool = False
    is_json_pointer: bool = False
    is_relative_json_pointer: bool = False
    is_regex: bool = False
    is_uri: bool = False
    is_uri_ref: bool = False
    is_uri_template: bool = False
    is_duration: bool = False
    pattern: str = None
    format: str = None