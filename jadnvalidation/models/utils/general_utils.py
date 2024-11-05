import re
from jsonpointer import JsonPointer, JsonPointerException
from validators import domain
from consts import ALLOWED_TYPE_OPTIONS


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
