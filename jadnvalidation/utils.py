from typing import List
from pydantic import Field
from consts import ALLOWED_TYPE_OPTIONS
from jadnvalidation.models.pyd.pyd_field_mapper import Pyd_Field_Mapper


def convert_to_pyd_type(type_str: str) -> type:
    """
    Converts a jadn type to its corresponding Python type.
    """
    type_mapping = {
        "String": str,
        "Integer": int,
        "Number": float,
        "Boolean": bool,
        "Array": list,
        "Record": dict
        # Add more mappings as needed
        # Binary?
    }
    return type_mapping.get(type_str, str)  # Default to string if type is unknown

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

def map_type_opts(type_opts: List[str]) -> Pyd_Field_Mapper:
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
                if opt_val == "date-time":
                    pyd_field_mapper.is_datetime = True
                elif opt_val == "date":
                    pyd_field_mapper.is_date = True
                elif opt_val == "time":
                    pyd_field_mapper.is_time = True                    
            case "%":           # pattern - Regular expression used to validate a String type (Section 3.2.1.6)
                pyd_field_mapper.pattern = opt_val
            case "y":           # minf - Minimum real number value (Section 3.2.1.7)
                py_field = ""
            case "z":           # maxf - Maximum real number value
                py_field = ""
            case "{":           # minv - Minimum integer value, octet or character count, or element count (Section 3.2.1.7)
                pyd_field_mapper.min_length = opt_val
            case "}":           # maxv - Maximum integer value, octet or character count, or element count
                pyd_field_mapper.max_length = opt_val
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