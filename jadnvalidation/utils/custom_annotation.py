import re
from typing import Annotated, Union
from pydantic import AnyHttpUrl, BeforeValidator, StringConstraints
from jsonpointer import JsonPointer, JsonPointerException
from uritemplate import URITemplate
from validators import domain

def validate_bytes(data: Union[str, bytes, bytearray]):
    bytes_data = data
    
    if isinstance(data, str):
        bytes_data = data.encode('utf-8')
    
    if isinstance(bytes_data, bytearray):
        if not all(0 <= byte <= 255 for byte in data):
            raise ValueError('Not valid byte array data, decoding error')
        
        bytes_data = bytes(data)
        try:
            bytes_data.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('Not valid byte data, decoding error from bytearray')        
        
    elif isinstance(bytes_data, bytes):    
        try:
            bytes_data.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('Not valid byte data, decoding error')
        
    else:
        raise ValueError('Not valid byte data')
           
    return bytes_data

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

def validate_str(val: str):
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

def validate_uri_template(val: str):
    """
    Validate URI Template - Implementation of RFC 6570 URI Templates
    """
    try:
        t = URITemplate(val)
        
        if not t.variables or len(t.variables) == 0:
            raise ValueError("URI Template missing template params")           
        if not isinstance(t, URITemplate):
            raise ValueError("Not a valid URI Template")         
        
    except Exception as ex:
        raise ValueError(f"Invalid URI Template: {ex}")
    
    return val

Hostname = Annotated[str, StringConstraints(pattern=r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")]
# Hostname = Annotated[str, BeforeValidator(validate_domain)]
IdnHostname = Annotated[str, BeforeValidator(validate_idn_domain)]
PydJsonPointer = Annotated[str, BeforeValidator(validate_json_pointer)]
PydRelJsonPointer = Annotated[str, BeforeValidator(validate_rel_json_pointer)]
PydRegex = Annotated[str, BeforeValidator(validate_regex)]
BinaryHex = Annotated[str, BeforeValidator(validate_hex)]
UriTemplate = Annotated[str, BeforeValidator(validate_uri_template)]

CustStr = Annotated[str, BeforeValidator(validate_str)]