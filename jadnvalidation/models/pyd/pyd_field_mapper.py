class Pyd_Field_Mapper():
    min_length: int = None
    max_length: int = None
    is_date: bool = False
    is_datetime: bool = False
    is_email: bool = False
    is_idn_email: bool = False
    is_time: bool = False
    is_hostname: bool = False
    is_idn_hostname: bool = False
    is_ipv4: bool = False
    is_ipv6: bool = False
    is_iri: bool = False
    is_iri_ref: bool = False
    is_uri: bool = False
    is_uri_ref: bool = False
    is_uri_template: bool = False
    pattern: str = None