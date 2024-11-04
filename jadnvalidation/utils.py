import re
from jsonpointer import JsonPointer, JsonPointerException
from validators import domain
from typing import Annotated, List
from pydantic import BeforeValidator, Field, StringConstraints
from consts import ALLOWED_TYPE_OPTIONS
from jadnvalidation.models.pyd.pyd_field_mapper import Pyd_Field_Mapper


def convert_to_pyd_type(type_str: str) -> type:
    """
    Converts a jadn type to its corresponding Python type.
    """
    type_mapping = {
        "Binary": str,
        "Boolean": bool,
        "Integer": Annotated [int, Field(strict=True, ge=None, le=None)],
        "Number": float,        
        "String": str,
        "Array": list,
        "Record": dict
        # Add more mappings as needed
    }
    return type_mapping.get(type_str, str)  # Default to string if type is unknown

def convert_binary_to_hex(binary_string):
    """Converts a binary string to its hexadecimal representation."""

    return hex(int(binary_string, 2))[2:]  # [2:] removes the '0x' prefix

def convert_list_to_dict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict

def get_jadn_type_opts(jadn_type_name: str) -> tuple:
    return ALLOWED_TYPE_OPTIONS.get(jadn_type_name)

def split_on_first_char(string):
    """Splits a string on the first character."""

    if not string:
        return []

    return [string[0], string[1:]]

# Not used yet, cannot failed '192.168.123.132' but should pass
def validate_domain(val: str):
    result = domain(val, rfc_2782=True)
    
    if not result:
        raise ValueError('Not a valid domain')
    
    return val

def validate_hex(cls, v):
    """
    The validate_hex function checks if all characters in the string are valid hexadecimal digits (0-9, A-F, a-f). 
    If not, it raises a ValueError.    
    """
    if not re.match(r'^[0-9a-fA-F]+$', v):
        raise ValueError('Invalid binary hex value')
    return v

def validate_idn_domain(val: str):
    result = domain(val, rfc_2782=True)
    
    if not result:
        raise ValueError('Not a valid idn-domain')
    
    return val

def validate_json_pointer(val: str):
    """
    Validate JSON Pointer - RFC 6901
    """
    try:
        res = JsonPointer(val)
        
        if not isinstance(res, JsonPointer):
            raise ValueError("Not a valid Json Pointer")    
        
    except JsonPointerException as ex:
        raise ValueError(ex)
    
    return val

def validate_rel_json_pointer(val: str):
    """
    Validate Relative JSON Pointer - RFC-8259
    """
    
    non_negative_integer, rest = [], ""
    for i, character in enumerate(val):
        if character.isdigit():
            non_negative_integer.append(character)
            continue
        if not non_negative_integer:
            raise ValueError("invalid relative json pointer given")
        rest = val[i:]
        break
    try:
        (rest == "#") or JsonPointer(rest)
    except JsonPointerException as ex:
        raise ValueError(ex)
    
    return val

def validate_regex(val: str):
    """
    Validate Regular Expression - ECMA 262
    """
    try:
        res = re.compile(val)
        
        if not isinstance(res, re.Pattern):
            raise ValueError("Not a valid regex")          
        
    except Exception as ex:
        raise ValueError(ex)
    
    return val

def map_type_opts(jdn_type: str, type_opts: List[str]) -> Pyd_Field_Mapper:
    pyd_field_mapper = Pyd_Field_Mapper()
    
    for type_opt in type_opts:
        
        opt_char_id, opt_val = split_on_first_char(type_opt)
        
        match opt_char_id:
            case "=":           # id - Items and Fields are denoted by FieldID rather than FieldName (Section 3.2.1.1)
                py_field = ""
            case "*":           # vtype - Value type for ArrayOf and MapOf (Section 3.2.1.2)
                py_field = ""
            case "+":           # ktype - Key type for MapOf (Section 3.2.1.3)
                py_field = ""
            case "#":           # enum -  Extension: Enumerated type derived from a specified type (Section 3.3.3)
                py_field = ""
            case ">":           # pointer - Extension: Enumerated type pointers derived from a specified type (Section 3.3.5)
                py_field = ""
            case "/":           # format - Semantic validation keyword (Section 3.2.1.5)   
                                             
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
                  
                elif opt_val == "duration":
                    pyd_field_mapper.is_duration = True
                    pyd_field_mapper.ge = 0
                elif opt_val == "i8":
                    pyd_field_mapper.ge = -128
                    pyd_field_mapper.le = 127
                elif opt_val == "i16":
                    pyd_field_mapper.ge = -32768
                    pyd_field_mapper.le = 32767
                elif opt_val == "i32":
                    pyd_field_mapper.ge = -2147483648
                    pyd_field_mapper.le = 2147483647
            case "%":           # pattern - Regular expression used to validate a String type (Section 3.2.1.6)
                pyd_field_mapper.pattern = opt_val
            case "y":           # minf - Minimum real number value (Section 3.2.1.7). Being deprecated for new JADN
                py_field = ""
            case "z":           # maxf - Maximum real number value. Being deprecated for new JADN,
                py_field = ""
            case "{":           # minv - Minimum integer value, octet or character count, or element count (Section 3.2.1.7)
                if jdn_type == "String":
                    try:
                        minv = int(opt_val)
                        pyd_field_mapper.min_length = minv
                    except TypeError as e:
                        print("Invalid option: requires integer value: " + e)
                elif jdn_type == "Integer" or jdn_type == "Number":
                    try:
                        minv = int(opt_val)
                        pyd_field_mapper.ge = minv
                    except TypeError as e:
                        print("Invalid option: requires integer value: " + e)
                        
            case "}":           # maxv - Maximum integer value, octet or character count, or element count
                if jdn_type == 'String':
                    try:
                        maxv = int(opt_val)
                        pyd_field_mapper.max_length = maxv
                    except TypeError as e:
                        print("Invalid option: requires integer value: " + e)
                elif jdn_type == "Integer" or jdn_type == "Number":
                    try:
                        maxv = int(opt_val)
                        pyd_field_mapper.le = maxv
                    except TypeError as e:
                        print("Invalid option: requires integer value: " + e)
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

# custom pyd types
Hostname = Annotated[str, StringConstraints(pattern=r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")]
# Hostname = Annotated[str, BeforeValidator(validate_domain)]
IdnHostname = Annotated[str, BeforeValidator(validate_idn_domain)]
PydJsonPointer = Annotated[str, BeforeValidator(validate_json_pointer)]
PydRelJsonPointer = Annotated[str, BeforeValidator(validate_rel_json_pointer)]
PydRegex = Annotated[str, BeforeValidator(validate_regex)]
BinaryHex = Annotated[str, BeforeValidator(validate_hex)]