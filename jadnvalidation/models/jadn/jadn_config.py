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