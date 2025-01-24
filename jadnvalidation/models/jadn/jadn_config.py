GLOBAL_CONFIG_KEY = "root_global_opts"

MAX_BINARY_KEY = "$MaxBinary"
MAX_STRING_KEY = "$MaxString"
MAX_ELEMENTS_KEY = "$MaxElements"
SYS_IND_KEY = "$Sys"
TYPE_NAME_KEY = "$TypeName"
FIELD_NAME_KEY = "$FieldName"
NSID_KEY = "$NSID"

DEFAULT_MAX_BINARY = 255
DEFAULT_MAX_STRING = 255
DEFAULT_MAX_ELEMENTS = 100
DEFAULT_SYS_IND = "$"
DEFAULT_TYPE_NAME_REGEX = "^[A-Z][-$A-Za-z0-9]{0,63}$"
DEFAULT_FIELD_NAME_REGEX = "^[a-z][_A-Za-z0-9]{0,63}$"
DEFAULT_NSID_REGEX = "^[A-Za-z][A-Za-z0-9]{0,7}$"

class Jadn_Config():
    MaxBinary: int = DEFAULT_MAX_BINARY
    MaxString: int = DEFAULT_MAX_STRING
    MaxElements: int = DEFAULT_MAX_ELEMENTS
    Sys: str = DEFAULT_SYS_IND
    TypeName: str = DEFAULT_TYPE_NAME_REGEX
    FieldName: str = DEFAULT_FIELD_NAME_REGEX
    NSID: str = DEFAULT_NSID_REGEX
    
    def __init__(self, MaxBinary = DEFAULT_MAX_BINARY, MaxString = DEFAULT_MAX_STRING, MaxElements = DEFAULT_MAX_ELEMENTS, Sys = DEFAULT_SYS_IND, TypeName = DEFAULT_TYPE_NAME_REGEX, FieldName = DEFAULT_FIELD_NAME_REGEX, NSID = DEFAULT_NSID_REGEX):
        self.MaxBinary = MaxBinary
        self.MaxString = MaxString    
        self.MaxElements = MaxElements    
        self.Sys = Sys
        self.TypeName = TypeName
        self.FieldName = FieldName
        self.NSID = NSID
        
def build_jadn_config_obj(j_config_data: dict) -> Jadn_Config:
    if j_config_data == None:
        j_config_data = {}
    
    j_config_obj = Jadn_Config(
        FieldName=j_config_data.get(FIELD_NAME_KEY, DEFAULT_FIELD_NAME_REGEX),
        MaxBinary=j_config_data.get(MAX_BINARY_KEY, DEFAULT_MAX_BINARY),
        MaxElements=j_config_data.get(MAX_ELEMENTS_KEY, DEFAULT_MAX_ELEMENTS),
        MaxString=j_config_data.get(MAX_STRING_KEY, DEFAULT_MAX_STRING),
        NSID=j_config_data.get(NSID_KEY, DEFAULT_NSID_REGEX),
        Sys=j_config_data.get(SYS_IND_KEY, DEFAULT_SYS_IND)
    )
    
    return j_config_obj