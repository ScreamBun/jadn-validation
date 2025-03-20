import inspect
from typing import Callable, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, ConfigDict, Field, model_validator

from jadnvalidation.utils.consts import ALLOWED_TYPE_OPTIONS, FIELD_OPTION_KEYS, MULTI_CHECK, NULL_ARGS, OPTION_ID, OPTIONS, REQUIRED_TYPE_OPTIONS, TYPE_OPTION_KEYS
from jadnvalidation.models.pyd.structures import ValidationFormats


class Options(BaseModel):
     
    # Custom Options 
    data_type: str = Field(exclude=True, default=None)                         #: Data type of the definition the options are attached
    name: Optional[str] = Field(exclude=True, default=None)                    #: Name of the definition the options are attached
    validation: Dict[str, Callable] = Field(ValidationFormats, exclude=True)   #: JADN format validators
    __custom__ = ["data_type", "name", "validation"]
    
    # Type Options
    id: Optional[bool] = None         #: `=` -> ASCII(61): Items and Fields are denoted by FieldID rather than FieldName (Section 3.2.1.1)
    vtype: Optional[str] = None       #: `*` -> ASCII(42): Value type for ArrayOf and MapOf (Section 3.2.1.2)
    ktype: Optional[str] = None       #: `+` -> ASCII(43): Key type for MapOf (Section 3.2.1.3)
    enum: Optional[str] = None        #: `#` -> ASCII(35): Extension: Enumerated type derived from a specified type (Section 3.3.3)
    pointer: Optional[str] = None     #: `>` -> ASCII(62): Extension: Enumerated type pointers derived from a specified type (Section 3.3.5)
    format: Optional[str] = None      #: `/` -> ASCII(47): Semantic validation keyword (Section 3.2.1.5)
    pattern: Optional[str] = None     #: `%` -> ASCII(37): Regular expression used to validate a String type (Section 3.2.1.6)
    minf: Optional[float] = None      #: `y` -> ASCII(121): Minimum real number value (Section 3.2.1.7)
    maxf: Optional[float] = None      #: `z` -> ASCII(122): Maximum real number value
    minv: Optional[int] = None        #: `{` -> ASCII(123): Minimum integer value, octet or character count, or element count (Section 3.2.1.7)
    maxv: Optional[int] = None        #: `}` -> ASCII(125): Maximum integer value, octet or character count, or element count
    unique: Optional[bool] = None     #: `q` -> ASCII(113): ArrayOf instance must not contain duplicate values (Section 3.2.1.8)
    set: Optional[bool] = None        #: `s` -> ASCII(115): ArrayOf instance is unordered and unique (Section 3.2.1.9)
    unordered: Optional[bool] = None  #: `b` -> ASCII(98): ArrayOf instance is unordered (Section 3.2.1.10)
    extend: Optional[bool] = None     #: `X` -> ASCII(88): Type is extensible; new Items or Fields may be appended (Section 3.2.1.11)
    default: Optional[str] = None     #: `!` -> ASCII(33): Default value (Section 3.2.1.12)
    
    # Field options
    minc: Optional[int] = Field(None, description="`[` -> ASCII(91): Minimum cardinality, default = 1, 0 = optional (Section 3.2.2.1)")
    maxc: Optional[int] = None        #: `]` -> ASCII(93): Maximum cardinality, default = 1, 0 = default max, >1 = array
    tagid: Optional[str] = None       # enumerated -> `&` -> ASCII(38): Field containing an explicit tag for this Choice type (Section 3.2.2.2)
    dir: Optional[bool] = None        #: `<` -> ASCII(60): Pointer enumeration treats field as a group of items (Extension: Section 3.3.5)
    key: Optional[bool] = None        #: `K` -> ASCII(75): Field is a primary key for this type (Extension: Section 3.3.6)
    link: Optional[bool] = None       #: `L` -> ASCII(76): Field is a foreign key reference to a type instance (Extension: Section 3.3.6)    
    

    def __init__(self, *args, **kwargs):
        data = {}
        for arg in args:
            if inspect.isclass(arg) or isinstance(arg, Options):
                keys = [*self.model_fields, *self.__custom__]
                data.update({k: getattr(arg, k) for k in keys if getattr(arg, k, None) not in NULL_ARGS})
            elif isinstance(arg, list):
                data.update(self.list2dict(arg))
            elif isinstance(arg, dict):
                data.update(arg)
        data.update(kwargs)
        super().__init__(**data) 

    def schema(self) -> List[str]: 
        """
        Format options into valid JADN format for the base type they are attached
        :return: JADN formatted options
        """
        return self.dict2list(self.model_dump(exclude_unset=True))

    # Validation
    @model_validator(mode='before')
    def validate_data(cls, opts: dict):
        """
        Pydantic validator - validate the options for the attached data type
        :param opts: options to validate
        :raise ValueError: invalid options given
        :return: original options
        """
        if fields := set(opts.keys()) - set(cls.__custom__) - set(FIELD_OPTION_KEYS):
            data_type = opts.get("data_type")
            if required := set(REQUIRED_TYPE_OPTIONS.get(data_type, ())):
                if missing := (required - fields):
                    raise ValueError(f"{data_type} missing required option of {missing.pop()}")
            if allowed := set(ALLOWED_TYPE_OPTIONS.get(data_type, ())):
                if extra := (fields - allowed):
                    raise ValueError(f"{data_type} has extra options of {extra}")
        return opts

    # Helpers
    @classmethod
    def dict2list(cls, opts: Dict[str, Union[bool, int, float, str]]) -> List[str]:
        """
        Convert dict formatted option into JADN format
        :param opts: key/value formatted options
        :raise KeyError: invalid option given
        :return:  JADN formatted options
        """
        rslt = []
        for field, val in opts.items():
            if val is not None:
                if val is True:
                    rslt.append(f"{OPTION_ID.get(field)}")
                else:
                    rslt.append(f"{OPTION_ID.get(field)}{val}")
        return rslt

    @classmethod
    def list2dict(cls, opts: List[str]) -> Dict[str, Union[bool, int, float, str]]:
        """
        Convert JADN formatted option in list format to a dict
        :param opts: JADN formatted options
        :raise KeyError: invalid option given
        :return: key/value formatted options
        """
        rslt = {}
        for opt in opts:
            key, val = opt[0], opt[1:]
            if args := OPTIONS.get(ord(key)):
                rslt[args[0]] = args[1](val)
            else:
                raise KeyError(f"Unknown option id of {key}")
        return rslt

    def isArray(self) -> bool:
        """
        Determine if the field is an array based on the given options
        :return: True/False if the field is an array
        """
        if self.ktype or self.vtype:
            return False
        maxc = self.maxc if isinstance(self.maxc, int) else 1
        return maxc != 1

    def isOptional(self) -> bool:
        """
        Determine if the field is optional
        :return: True/False if the field is optional
        """
        
        isOpt = True
        if self.minc is not None:
            
            if self.minc >= 1:
                isOpt = False
        
        return isOpt

    def isRequired(self) -> bool:
        """
        Determine if the field is required
        :return: True/False if the field is required
        """
        return not self.isOptional()

    def multiplicity(self, min_default: int = 0, max_default: int = 0, field: bool = False, check=MULTI_CHECK) -> str:
        """
        Determine the multiplicity of the min/max options

        | minc | maxc | Multiplicity | Description                             | Keywords                    |
        | ---- | ---- | ------------ | --------------------------------------- | --------------------------- |
        | 0    | 1    | 0..1         | No instances or one instance            | optional                    |
        | 1    | 1    | 1            | Exactly one instance                    | required                    |
        | 0    | 0    | 0..*         | Zero or more instances                  | optional, repeated          |
        | 1    | 0    | 1..*         | At least one instance                   | required, repeated          |
        | m    | n    | m..n         | At least m but no more than n instances | required, repeated if m > 1 |

        :param min_default: default value of minc/minv
        :param max_default: default value of maxc/maxv
        :param field: if option for field or type
        :param check: function for ignoring multiplicity - Fun(minimum, maximum) -> bool
        :return: options multiplicity or empty string
        """
        minKey, maxKey = ("minc", "maxc") if field else ("minv", "maxv")
        minimum = getattr(self, minKey, min_default) or min_default
        maximum = getattr(self, maxKey, max_default) or max_default
        if check(minimum, maximum):
            if minimum == 1 and maximum == 1:
                return "1"
            return f"{minimum}..{'*' if maximum == 0 else maximum}"
        return ""

    def numeric_limit(self, min_default: Union[int, float] = None, max_default: Union[int, float] = None) -> str:
        """
        Get the numeric limit of the options
        :param min_default: default minimum
        :param max_default: default maximum
        :return: numeric limits or empty string
        """
        minKey, maxKey = ("minv", "maxv") if self.data_type == "Integer" else ("minf", "maxf")
        minimum = getattr(self, minKey, min_default)
        maximum = getattr(self, maxKey, max_default)

        if minimum is None and maximum is None:
            return ""
        if minimum is None and maximum is not None:
            return f"*..{maximum}"
        if minimum is not None and maximum is None:
            return f"{minimum}..*"
        return f"{minimum}..{maximum}"

    def setdefault(self, name: str, default: Union[bool, int, float, str] = None) -> Union[bool, int, float, str]:
        if val := getattr(self, name, None):
            return val
        setattr(self, name, default)
        return self[name]

    def split(self) -> Tuple["Options", "Options"]:
        """
        Split the options into Field options and Type options
        :return: Tuple of Field & Type options
        """
        field_opts = Options({f: self[f] for f in self.model_fields if f in FIELD_OPTION_KEYS and self[f] is not None})
        type_opts = Options({f: self[f] for f in self.model_fields if f in TYPE_OPTION_KEYS if self[f] is not None})
        return field_opts, type_opts

    # class Config:
    #     smart_union = True
    #     fields = {
    #         "data_type": {"exclude": True},
    #         "name": {"exclude": True},
    #         "validation": {"exclude": True}
    #     }    