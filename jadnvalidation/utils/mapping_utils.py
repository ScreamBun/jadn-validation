from typing import List, Union
from math import pow
from pydantic import StrictBool, StrictBytes, StrictFloat, StrictInt, StrictStr

from jadnvalidation.models.jadn.jadn_field import Jadn_Field
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type
from jadnvalidation.models.pyd.pyd_field_mapper import Pyd_Field_Mapper
from jadnvalidation.utils import general_utils
from jadnvalidation.utils.consts import Choice_Consts


def convert_to_pyd_type(type_str: str) -> type:
    
    # Converts a jadn type to its corresponding Pydantic type.
    
    type_mapping = {
        Base_Type.STRING.value: StrictStr,
        # Base_Type.BINARY.value: Annotated [bytes, BeforeValidator(validate_bytes), Field(strict=True, ge=None, le=None)],
        Base_Type.BINARY.value: StrictBytes,
        Base_Type.BOOLEAN.value: StrictBool,
        # Base_Type.INTEGER.value: Annotated [int, Field(strict=True, ge=None, le=None)],
        Base_Type.INTEGER.value: StrictInt,
        # Base_Type.NUMBER.value: Annotated [float, Field(strict= True, ge=None, le=None)],
        Base_Type.NUMBER.value: StrictFloat,
        Base_Type.ARRAY.value: list,
        Base_Type.RECORD.value: dict
        # Add more mappings as needed
    }
    return type_mapping.get(type_str, str)  # Default to string if type is unknown


def convert_to_python_type(type_str: str) -> type:
    """
    Converts a jadn type to its corresponding Python type.
    """
    type_mapping = {
        Base_Type.STRING.value: str,
        Base_Type.BINARY.value: bytes,
        Base_Type.BOOLEAN.value: bool,
        Base_Type.INTEGER.value: int,
        Base_Type.NUMBER.value: float,
        Base_Type.ARRAY.value: list,
        Base_Type.RECORD.value: dict
    }
    return type_mapping.get(type_str, str)

def get_choice_type(j_type_opts: List[str]) -> str:
    choice_type = Choice_Consts.CHOICE_ONE_OF
    
    for type_opt in j_type_opts:
        opt_char_id, opt_val = general_utils.split_on_first_char(type_opt) 
        if opt_char_id == "A":
            choice_type = Choice_Consts.CHOICE_ALL_OF
        elif opt_char_id == "O":
            choice_type = Choice_Consts.CHOICE_ANY_OF
        elif opt_char_id == "X":
            choice_type = Choice_Consts.CHOICE_NOT
        else:
            choice_type = Choice_Consts.CHOICE_ONE_OF
            
        break
        
    return choice_type

def get_max_length(j_type: Jadn_Type) -> int:
    
    if j_type.base_type == Base_Type.STRING.value:
        max_length = j_type.config.MaxString
    elif j_type.base_type == Base_Type.BINARY.value:
        max_length = j_type.config.MaxBinary
    else:
        max_length = None
    
    opts = get_opts(j_type)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "}" == opt_key:
            max_length = int(opt_val)
            break
        
    return max_length
            
def get_min_length(j_type: Jadn_Type) -> int:
    min_length = None
    
    opts = get_opts(j_type)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "{" == opt_key:
            min_length = int(opt_val)
            break
    
    # for type_opt in j_type_opts:
    #     opt_char_id, opt_val = general_utils.split_on_first_char(type_opt) 
    #     if opt_char_id == "{":
    #         try:
    #             min_length = int(opt_val)
    #         except ValueError as e:
    #             print("Invalid option: requires integer value: " + e)
    #         break   
    #     elif opt_char_id == "/":
    #         try:
    #             format_minv = get_format_min(opt_val)
    #             if min_length and min_length < format_minv:
    #                 min_length = format_minv
    #         except ValueError as e:
    #             print("Error getting requirements for {optval} format:" + e)
    
    return min_length  

def get_min_occurs(j_type: Jadn_Type) -> int:
    min_occurs = None
    
    opts = get_opts(j_type)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "[" == opt_key:
            try:
                min_occurs = int(opt_val)
            except ValueError as e:
                print("Invalid option: requires integer value: " + e)
            break
    
    return min_occurs  

def get_max_occurs(j_type: Jadn_Type) -> int:
    max_occurs = None
    
    opts = get_opts(j_type)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "]" == opt_key:
            try:
                max_occurs = int(opt_val)
            except ValueError as e:
                print("Invalid option: requires integer value: " + e)
            break   

    
    return max_occurs  

def get_min_max(global_configs, type_opts): #sword of damocles for deprecation
    min_elements = None
    max_elements = None
    
    if global_configs and global_configs.MaxElements:
        max_elements = global_configs.MaxElements
    
    if type_opts and type_opts.max_length:
        max_elements = type_opts.max_length
    elif type_opts and type_opts.le:
        max_elements = type_opts.le
            
    if type_opts and type_opts.min_length:
        min_elements = type_opts.min_length
    elif type_opts and type_opts.ge:
        min_elements = type_opts.ge
        
    return min_elements, max_elements 

def get_opts(j_type: Jadn_Type):
    opts = None
    if isinstance(j_type, Jadn_Type):
        opts = j_type.type_options
        
    return opts

def get_type(j_obj: Union[Jadn_Type, Jadn_Field]):
    type = None
    if isinstance(j_obj, Jadn_Type):
        opts = j_obj.type_name
    elif isinstance(j_obj, Jadn_Field):
        opts = j_obj.type
        
    return opts

def get_ktype(j_obj: Union[Jadn_Type, Jadn_Field]):
    val = None
    opts = get_opts(j_obj)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "+" == opt_key:
            val = opt_val
            break
        
    return val

def get_vtype(j_obj: Union[Jadn_Type, Jadn_Field]):
    val = None
    opts = get_opts(j_obj)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "*" == opt_key:
            val = opt_val
            break
        
    return val

def is_optional(j_type: Jadn_Type) -> bool:
    is_optional = False
    
    # TODO: Need logic for min_occurs?
    
    min = get_min_length(j_type)
    if min == 0:
        is_optional = True
    
    return is_optional

def get_format(j_type: Jadn_Type):
    val = None
    opts = get_opts(j_type)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "/" == opt_key:
            val = opt_val
            break
        
    return val

def get_format_min(format: str):
    format_min = None
    format_min = give_format_constraint(format, 0)
    return format_min

def get_format_max(format: str):
    format_max = None
    format_max = give_format_constraint(format, 1)
    return format_max
    
def give_format_constraint(format: str, option_index: int):

    format_designator, designated_value = general_utils.split_on_first_char(format) 
    
    format_constraints = {
        "i8": [-127, 128],
        "i16": [-32768, 32767],
        "i32": [-2147483648, 2147483647],
        
        }
    if format in format_constraints.keys:
        return format_constraints(format[option_index])
    
    elif format_designator == "u":
        try:
            unsigned_value = int(designated_value)
            print("uN value is 2^"+str(unsigned_value))
            unsig_min = 0
            unsig_max = pow(2,unsigned_value)
            struct = [unsig_min, unsig_max]
            return struct[option_index]
        except ValueError as e:
            print("u<n> format requires a numeric component following unsigned signifier \"u\". \n"+e)
    else: return None

def map_type_opts(j_type: str, j_type_opts: List[str]) -> Pyd_Field_Mapper:
    pyd_field_mapper = Pyd_Field_Mapper()
    
    for type_opt in j_type_opts:
        
        opt_char_id, opt_val = general_utils.split_on_first_char(type_opt)
        
        match opt_char_id:
            case "=":           # id - Items and Fields are denoted by FieldID rather than FieldName (Section 3.2.1.1)
                pyd_field_mapper.use_field_id = True
            case "*":           # vtype - Value type for ArrayOf and MapOf (Section 3.2.1.2)
                py_field = ""
            case "+":           # ktype - Key type for MapOf (Section 3.2.1.3)
                py_field = ""
            case "#":           # enum -  Extension: Enumerated type derived from a specified type (Section 3.3.3)
                py_field = ""
            case ">":           # pointer - Extension: Enumerated type pointers derived from a specified type (Section 3.3.5)
                py_field = ""
            case "/":           # format - Semantic validation keyword (Section 3.2.1.5)   
                      
                # String                       
                if opt_val == "date":
                    pyd_field_mapper.is_date = True
                elif opt_val == "date-time":
                    pyd_field_mapper.is_datetime = True
                elif opt_val == "time":
                    pyd_field_mapper.is_time = True                                       
                elif opt_val == "email":
                    pyd_field_mapper.is_email = True
                elif opt_val == "idn-email":
                    pyd_field_mapper.is_idn_email = True
                elif opt_val == "hostname":
                    pyd_field_mapper.is_hostname = True
                elif opt_val == "idn-hostname":
                    pyd_field_mapper.is_idn_hostname = True
                elif opt_val == "ipv4":
                    pyd_field_mapper.is_ipv4 = True
                elif opt_val == "ipv6":
                    pyd_field_mapper.is_ipv6 = True
                elif opt_val == "iri":
                    pyd_field_mapper.is_iri = True
                elif opt_val == "iri-reference":
                    pyd_field_mapper.is_iri_ref = True
                elif opt_val == "json-pointer":
                    pyd_field_mapper.is_json_pointer = True
                elif opt_val == "relative-json-pointer":
                    pyd_field_mapper.is_relative_json_pointer = True
                elif opt_val == "regex":
                    pyd_field_mapper.is_regex = True                                                                                                
                elif opt_val == "uri":
                    pyd_field_mapper.is_uri = True
                elif opt_val == "uri-reference":
                    pyd_field_mapper.is_uri_ref = True
                elif opt_val == "uri-template":
                    pyd_field_mapper.is_uri_template = True

                # Binary
                elif opt_val == "eui":
                    pyd_field_mapper.is_eui = True
                elif opt_val == "ipv4-addr":
                    pyd_field_mapper.is_ipv4_addr = True
                elif opt_val == "ipv6-addr":
                    pyd_field_mapper.is_ipv6_addr = True                                                                                                                                                                                                   
                  
                # Integer  
                elif opt_val == "duration":
                    pyd_field_mapper.is_duration = True
                    pyd_field_mapper.min_length = 0
                    set_min_length(0, j_type, pyd_field_mapper)
                elif opt_val == "i8":
                    pyd_field_mapper.min_length = -128
                    set_min_length(-128, j_type, pyd_field_mapper)
                    pyd_field_mapper.max_length = 127
                    set_max_length(127, j_type, pyd_field_mapper)
                elif opt_val == "i16":
                    pyd_field_mapper.min_length = -32768
                    set_min_length(-32768, j_type, pyd_field_mapper)
                    pyd_field_mapper.max_length = 32767
                    set_max_length(32767, j_type, pyd_field_mapper)
                elif opt_val == "i32":
                    pyd_field_mapper.min_length = -2147483648
                    set_min_length(-2147483648, j_type, pyd_field_mapper)
                    pyd_field_mapper.max_length = 2147483647
                    set_max_length(2147483647, j_type, pyd_field_mapper)
                elif j_type == "Integer":
                    format_designator, possible_unsigned = general_utils.split_on_first_char(opt_val) 
                    if format_designator == "u":
                        try:
                            unsigned_value = int(possible_unsigned)
                            print("uN value is 2^"+str(unsigned_value))
                            pyd_field_mapper.ge = 0
                            pyd_field_mapper.le = pow(2,unsigned_value)
                        except ValueError as e:
                            print("u<n> format requires a numeric component following unsigned signifier \"u\". \n"+e)

            case "%":           # pattern - Regular expression used to validate a String type (Section 3.2.1.6)
                pyd_field_mapper.pattern = opt_val
            case "y":           # minf - Minimum real number value (Section 3.2.1.7). Being deprecated for new JADN
                py_field = ""
            case "z":           # maxf - Maximum real number value. Being deprecated for new JADN,
                py_field = ""
            case "{": 
                set_min_length(opt_val, j_type, pyd_field_mapper)
                
                if opt_val:
                    if int(opt_val) == 0:
                        pyd_field_mapper.is_optional = True
                
            case "}": 
                set_max_length(opt_val, j_type, pyd_field_mapper)
            case "[": 
                set_min_occurs(opt_val, j_type, pyd_field_mapper)
                
                if opt_val:
                    if int(opt_val) == 0:
                        pyd_field_mapper.is_optional = False
            case "]": 
                set_max_occurs(opt_val, j_type, pyd_field_mapper)                                   
            case "q":           # unique - ArrayOf instance must not contain duplicate values (Section 3.2.1.8)
                py_field = ""
            case "s":           # set - ArrayOf instance is unordered and unique (Section 3.2.1.9)
                py_field = ""
            case "b":           # unordered - ArrayOf instance is unordered (Section 3.2.1.10)
                py_field = ""
            case "X":           # extend - Type is extensible; new Items or Fields may be appended (Section 3.2.1.11)
                py_field = ""
            case "!":           # default - Default value (Section 3.2.1.12)
                py_field = ""                
            case default: 
                py_field = ""
                
    return pyd_field_mapper
            
def set_max_length(opt_val: str, j_type: str, p_field_mapper: Pyd_Field_Mapper): # kevin is updating 
        # Custom limits
    try:
        maxv = int(opt_val)
        p_field_mapper.max_length = maxv
    except TypeError as e:
            print("Invalid option: requires integer value: " + e)        
            
def set_min_length(opt_val: str, j_type: str, p_field_mapper: Pyd_Field_Mapper): # kevin is updating
    # Custom limits
    try:
        minv = int(opt_val)
        p_field_mapper.min_length = minv
    except TypeError as e:
        print("Invalid option: requires integer value: " + e)    

def set_min_occurs(opt_val: str, j_type: str, p_field_mapper: Pyd_Field_Mapper): # kevin is updating 
    try:
        minc = int(opt_val)
        p_field_mapper.min_occurs = minc
        if minc == 0:
            p_field_mapper.is_optional = True
    except TypeError as e:
        print("Invalid option: requires integer value: " + e) 


def set_max_occurs(opt_val: str, j_type: str, p_field_mapper: Pyd_Field_Mapper): # kevin is updating 
    try:
        maxc = int(opt_val)
        p_field_mapper.max_occurs = maxc
    except TypeError as e:
        print("Invalid option: requires integer value: " + e)    

def use_field_ids(j_type_opts: List[str]) -> bool:
    use_id = False
    
    if j_type_opts:
        for type_opt in j_type_opts:
            opt_char_id, opt_val = general_utils.split_on_first_char(type_opt)
            if opt_char_id == "=":
                use_id = True
                break   
    
    return use_id