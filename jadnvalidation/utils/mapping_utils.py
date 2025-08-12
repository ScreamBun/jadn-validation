import sys
from typing import List

from jadnvalidation.models.jadn.jadn_config import Jadn_Config
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type
from jadnvalidation.utils import general_utils
from jadnvalidation.utils.consts import Choice_Consts


def flip_to_array_of(j_type_obj: Jadn_Type, min_occurs, max_occurs):
    """
    Field type changes to an array of that type; array length equals max occurs.
    """
    array_vtype = "*" + j_type_obj.base_type
    array_min_len = "{" + str(min_occurs)
    array_max_len = "}" + str(max_occurs)
    
    j_field_obj = Jadn_Type(j_type_obj.type_name, Base_Type.ARRAY_OF.value)
    j_field_obj.type_options = []
    j_field_obj.type_options.append(array_vtype)
    j_field_obj.type_options.append(array_min_len)
    j_field_obj.type_options.append(array_max_len)    
    
    return j_field_obj


def derive_enum(j_type_obj: Jadn_Type, min_occurs, max_occurs):
    """
    Field type changes to an array of that type; array length equals max occurs.
    """
    enum_vtype = "*" + j_type_obj.base_type
    array_min_len = "{" + str(min_occurs)
    array_max_len = "}" + str(max_occurs)
    
    j_field_obj = Jadn_Type(j_type_obj.type_name, Base_Type.ARRAY_OF.value)
    j_field_obj.type_options = []
    j_field_obj.type_options.append(array_vtype)
    j_field_obj.type_options.append(array_min_len)
    j_field_obj.type_options.append(array_max_len)    
    
    return j_field_obj

def get_choice_type(j_type_opts: List[str]) -> str:
    choice_type = Choice_Consts.CHOICE_ONE_OF
    
    for type_opt in j_type_opts:
        opt_char_id, opt_val = general_utils.split_on_first_char(type_opt) 
        if (opt_char_id == "C") & (opt_val == "A"):
            choice_type = Choice_Consts.CHOICE_ALL_OF
        elif (opt_char_id == "C") & (opt_val == "O"):
            choice_type = Choice_Consts.CHOICE_ANY_OF
        elif (opt_char_id == "C") & (opt_val == "X"):
            choice_type = Choice_Consts.CHOICE_NOT  
        else:
            choice_type = Choice_Consts.CHOICE_ONE_OF
            
        break
        
    return choice_type

def get_max_length(j_type: Jadn_Type, global_config: Jadn_Config = None) -> int:
    
    if j_type.base_type == Base_Type.STRING.value:
        max_length = global_config.MaxString
    elif j_type.base_type == Base_Type.BINARY.value:
        max_length = global_config.MaxBinary
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
    min_val = get_opt_int("{", j_type)
    # if min_val == None:
    #     min_val = 0    
    return min_val

def get_min_occurs(j_type: Jadn_Type) -> int:
    min_val = get_opt_int("[", j_type)
    if min_val == None:
        min_val = 1
    return min_val

def get_max_occurs(j_type: Jadn_Type, global_config: Jadn_Config) -> int:
    max_val = get_opt_int("]", j_type)
    min_val = get_min_occurs(j_type)
    
    if min_val == None and max_val == None:
        max_val = 1
    elif min_val >= 0 and max_val == None:
        max_val = min_val
    elif max_val == -1:
        max_val = global_config.MaxElements
    elif max_val == -2:
        max_val = sys.maxsize
        
    return max_val

def get_min_inclusive(j_type: Jadn_Type) -> int:   
    return get_opt_int("w", j_type)

def get_max_inclusive(j_type: Jadn_Type) -> int:   
    return get_opt_int("x", j_type)

def get_min_exclusive(j_type: Jadn_Type) -> int:   
    return get_opt_int("y", j_type)

def get_max_exclusive(j_type: Jadn_Type) -> int:   
    return get_opt_int("z", j_type)

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
    opts = []
    
    if isinstance(j_type, Jadn_Type):
        opts = j_type.type_options
        
    # Check if opts is None or contains an empty string
    if opts is None or opts == [""]:
        opts = []  # Set opts to an empty list
        
    return opts

def get_opt_int(key: str, j_type: Jadn_Type):
    return_val = None
    opts = get_opts(j_type)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if key == opt_key:
            try:
                return_val = int(opt_val)
            except ValueError as e:
                print("Invalid option: requires integer value: " + e)
            break
        
    return return_val

def get_opt_str(key: str, j_type: Jadn_Type):
    return_val = None
    opts = get_opts(j_type)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if key == opt_key:
            return_val = opt_val
            break
        
    return return_val

def get_type(j_obj: Jadn_Type):
    type = None
    if isinstance(j_obj, Jadn_Type):
        opts = j_obj.type_name
        
    return opts

def get_ktype(j_obj: Jadn_Type):
    val = None
    opts = get_opts(j_obj)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "+" == opt_key:
            val = opt_val
            break
        
    return val

def get_vtype(j_obj: Jadn_Type):
    val = None
    opts = get_opts(j_obj)
    for opt in opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if "*" == opt_key:
            val = opt_val
            break
        
    return val

# Note: A separate function may be needed for optional structures
# This function is geared towards fields
def is_optional(j_type: Jadn_Type) -> bool: 
    is_optional = False
    
    min_occurs = get_min_occurs(j_type)
    min_length = get_min_length(j_type)
    
    if min_length == 0 or min_occurs == 0:
        is_optional = True
    
    return is_optional

def get_format(j_type: Jadn_Type):
    return get_opt_str("/", j_type)

def get_pattern(j_type: Jadn_Type):
    return get_opt_str("%", j_type)

def use_field_ids(j_type_opts: List[str]) -> bool:
    use_id = False
    
    if j_type_opts:
        for type_opt in j_type_opts:
            opt_char_id, opt_val = general_utils.split_on_first_char(type_opt)
            if opt_char_id == "=":
                use_id = True
                break   
    
    return use_id