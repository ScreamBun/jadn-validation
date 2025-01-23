from typing import List
from math import pow
from pydantic import StrictBool, StrictBytes, StrictFloat, StrictInt, StrictStr

from jadnvalidation.models.jadn.jadn_type import Base_Type
from jadnvalidation.models.pyd.pyd_field_mapper import Pyd_Field_Mapper
from jadnvalidation.utils import general_utils


def convert_to_pyd_type(type_str: str) -> type:
    """
    Converts a jadn type to its corresponding Python type.
    """
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

def set_max_length(opt_val: str, j_type: str, p_field_mapper: Pyd_Field_Mapper):
    if j_type in [Base_Type.STRING.value, Base_Type.BINARY.value, Base_Type.RECORD.value]:   
        # Custom limits
        try:
            maxv = int(opt_val)
            p_field_mapper.max_length = maxv
        except TypeError as e:
            print("Invalid option: requires integer value: " + e)
    elif j_type == Base_Type.INTEGER.value or j_type == Base_Type.NUMBER.value:
        try:
            maxv = int(opt_val)
            p_field_mapper.le = maxv
        except TypeError as e:
            print("Invalid option: requires integer value: " + e)
            
def set_min_length(opt_val: str, j_type: str, p_field_mapper: Pyd_Field_Mapper):
    # Custom limits
    if j_type in [Base_Type.STRING.value, Base_Type.BINARY.value, Base_Type.RECORD.value]:
        try:
            minv = int(opt_val)
            p_field_mapper.min_length = minv
        except TypeError as e:
            print("Invalid option: requires integer value: " + e)
    elif j_type == Base_Type.INTEGER.value or j_type == Base_Type.NUMBER.value:
        try:
            minv = int(opt_val)
            p_field_mapper.ge = minv
        except TypeError as e:
            print("Invalid option: requires integer value: " + e)

def map_type_opts(j_type: str, j_type_opts: List[str]) -> Pyd_Field_Mapper:
    pyd_field_mapper = Pyd_Field_Mapper()
    
    for type_opt in j_type_opts:
        
        opt_char_id, opt_val = general_utils.split_on_first_char(type_opt)
        
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
            case "}": 
                set_max_length(opt_val, j_type, pyd_field_mapper)
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