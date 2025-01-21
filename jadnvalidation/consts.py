from typing import Callable, Union
from jadnvalidation.utils.ext_dicts import FrozenDict


ALLOWED_TYPE_OPTIONS = {
    # Primitives
    "Binary" : ["{", "}", "/"], 
    "Boolean": [],
    "Integer": ["{", "}", "/"],
    "Number": ["y", "z", "/"], 
    "String": ["{", "}", "/", "%"],
    # Structures
    "Array": ["X", "/", "{", "}"],
    "ArrayOf": ["*", "{", "}", "q", "s", "b"],
    "Choice": ["=", "X"],
    "Enumerated": ["=", "#", ">", "X"],
    "Map": ["=", "X", "{", "}"],
    "MapOf": ["+", "*", "{", "}"],
    "Record": ["X", "{", "}"]
}

DYNAMIC_MODEL = "DynamicModel"
HOSTNAME_MAX_LENGTH = 255

NULL_ARGS = (None, "")
MULTI_CHECK: Callable[[int, int], bool] = lambda x, y: True

# Option Tags/Keys
#   JADN TypeOptions and FieldOptions contain a list of strings, each of which is an option.
#   The first character of an option string is the type ID; the remaining characters are the value.
#   The option string is converted into a Name: Value pair before use.
#   The tables list the unicode codepoint of the ID and the corresponding Name and value type.
#TODO: Replace FrozenDict
TYPE_OPTIONS = FrozenDict({        # Option ID: (name, value type, canonical order) # ASCII ID
    61: ("id", lambda x: True, 1),          # "=", Enumerated type and Choice/Map/Record keys are ID not Name
    42: ("vtype", lambda x: x, 2),          # "*", Value type for ArrayOf and MapOf
    43: ("ktype", lambda x: x, 3),          # "+", Key type for MapOf
    35: ("enum", lambda x: x, 4),           # "#", enumeration derived from Array/Choice/Map/Record type
    62: ("pointer", lambda x: x, 5),        # ">", enumeration of pointers derived from Array/Choice/Map/Record type
    47: ("format", lambda x: x, 6),         # "/", semantic validation keyword, may affect serialization
    37: ("pattern", lambda x: x, 7),        # "%", regular expression that a string must match
    121: ("minf", float, 8),                # "y", minimum Number value
    122: ("maxf", float, 9),                # "z", maximum Number value
    123: ("minv", int, 10),                 # "{", minimum byte or text string length, Integer value, element count
    125: ("maxv", int, 11),                 # "}", maximum byte or text string length, Integer value, element count
    113: ("unique", lambda x: True, 12),    # "q", ArrayOf instance must not contain duplicates
    115: ("set", lambda x: True, 13),       # "s", ArrayOf instance is unordered and unique
    98: ("unordered", lambda x: True, 14),  # "b", ArrayOf instance is unordered and not unique (bag)
    88: ("extend", lambda x: True, 15),     # "X", Type has an extension point where fields may be appended
    33: ("default", lambda x: x, 16),       # "!", Default or constant value of instances of this type
})

#TODO: Replace FrozenDict
FIELD_OPTIONS = FrozenDict({
    91: ("minc", int, 19),                  # "[", minimum cardinality, default = 1, 0 = field is optional
    93: ("maxc", int, 20),                  # "]", maximum cardinality, default = 1, 0 = inherited max, not 1 = array
    38: ("tagid", int, 21),                 # "&", field that specifies the type of this field
    60: ("dir", lambda x: True, 22),        # "<", pointer enumeration treats field as a collection
    75: ("key", lambda x: True, 23),        # "K", field is a primary key for this type
    76: ("link", lambda x: True, 24)        # "L", field is a link (foreign key) to an instance of FieldType
})

TYPE_OPTION_KEYS = tuple(v[0] for v in TYPE_OPTIONS.values())
FIELD_OPTION_KEYS = tuple(v[0] for v in FIELD_OPTIONS.values())

#TODO: Replace FrozenDict
OPTIONS = FrozenDict({**TYPE_OPTIONS, **FIELD_OPTIONS})
# Pre-computed reverse index - MUST match TYPE_OPTIONS and FIELD_OPTIONS
#TODO: Replace FrozenDict
OPTION_ID = FrozenDict({v[0]: chr(k) for k, v in OPTIONS.items()})
#TODO: Replace FrozenDict
ID_OPTIONS = FrozenDict({v: k for k, v in OPTION_ID.items()})

#TODO: Replace FrozenDict
REQUIRED_TYPE_OPTIONS = FrozenDict(
    # Primitives
    Binary=(),
    Boolean=(),
    Integer=(),
    Number=(),
    String=(),
    # Structures
    Array=(),
    ArrayOf=("vtype", ),
    Choice=(),
    Enumerated=(),
    Map=(),
    MapOf=("ktype", "vtype"),
    Record=()
)