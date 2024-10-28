class Pyd_Field_Mapper():
    min_length: int = None
    max_length: int = None
    is_date: bool = False
    is_datetime: bool = False
    is_email: bool = False
    is_idn_email: bool = False
    is_time: bool = False
    is_hostname: bool = False
    pattern: str = None