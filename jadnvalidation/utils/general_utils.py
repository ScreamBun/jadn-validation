import re
import sys
import importlib

from typing import Callable, Union

def addKey(d: dict, k: str = None) -> Callable:
    """
    Decorator to append a function to a dict, referencing the function name or given key as the key in the dict
    :param d: dict to append the key/func onto
    :param k: key to use on the dict
    :return: original function
    """
    def wrapped(fun: Callable, key: str = k) -> Callable:
        d[key if key else fun.__name__] = fun
        return fun
    return wrapped

def all_unique(lst):
  return len(lst) == len(set(lst))

def create_regex(pattern_string):
  try:
    return re.compile(pattern_string)
  except re.error as e:
    raise ValueError(f"Invalid regex pattern: {e}")
    
# (class_name, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None)
def create_clz_instance(class_name: str, *args, **kwargs):
    modules = {
        "Array" : "jadnvalidation.data_validation.array",
        "ArrayOf" : "jadnvalidation.data_validation.array_of",
        "Binary" : "jadnvalidation.data_validation.binary",
        "Boolean" : "jadnvalidation.data_validation.boolean",
        "Choice" : "jadnvalidation.data_validation.choice",
        "Enumerated" : "jadnvalidation.data_validation.enumerated",
        "Integer" : "jadnvalidation.data_validation.integer",
        "Map" : "jadnvalidation.data_validation.map",
        "MapOf" : "jadnvalidation.data_validation.map_of",
        "Number" : "jadnvalidation.data_validation.number",
        "Record" : "jadnvalidation.data_validation.record",
        "String" : "jadnvalidation.data_validation.string"
    }

    module = importlib.import_module(modules.get(class_name))
    
    if module == None:
        raise ValueError("Unknown data type")
    
    cls = getattr(module, class_name)
    
    return cls(*args, **kwargs)

def format_class_name(class_name: str) -> str:
    """
    Formats the class name by converting it to camelCase and then to titleCase.
    Removes '_' and '-' characters in the process.
    """
    # Remove '_' and '-' and split into words
    words = class_name.replace("_", " ").replace("-", " ").split()
   
    # Title each word and concatenate them into one word
    formatted_class_name = ''.join(word.title() for word in words)
    
    return formatted_class_name

def create_fmt_clz_instance(class_name: str, *args, **kwargs):
    
    modules = {
        "Date" : "jadnvalidation.data_validation.formats.date",
        "DateTime" : "jadnvalidation.data_validation.formats.date_time",
        "Time" : "jadnvalidation.data_validation.formats.time",
        "Ipv4" : "jadnvalidation.data_validation.formats.ipv4",
        "Ipv6" : "jadnvalidation.data_validation.formats.ipv6",
        "Email" : "jadnvalidation.data_validation.formats.email",
        "Hostname" : "jadnvalidation.data_validation.formats.hostname",
        "IdnEmail" : "jadnvalidation.data_validation.formats.idn_email",
        "IdnHostname" : "jadnvalidation.data_validation.formats.idn_hostname",
        "Eui" : "jadnvalidation.data_validation.formats.eui",
        "Pattern" : "jadnvalidation.data_validation.formats.pattern",
        "Regex" : "jadnvalidation.data_validation.formats.regex"
    }
    
    formatted_class_name = format_class_name(class_name)
    module = importlib.import_module(modules.get(formatted_class_name))
    
    if module == None:
        raise ValueError("Unknown format type")
    
    cls = getattr(module, formatted_class_name)
    
    return cls(*args, **kwargs)

def convert_binary_to_hex(binary_string):
    """Converts a binary string to its hexadecimal representation."""

    return hex(int(binary_string, 2))[2:]  # [2:] removes the '0x' prefix

def convert_list_to_dict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict

def create_dynamic_union(*types):
    return Union[types]

def get_data_by_id(data: dict, id: int):
    return data.get(str(id))

def get_data_by_name(data: dict, name: str):
    return data.get(name)

def get_item_safe_check(my_list, index):
    if 0 <= index < len(my_list):
        return my_list[index]
    return None  # Or any other default value

# TODO: We might be able to generalize this function
def get_choice_data_content(data: dict):
    '''
    Choice Data Example:
        "Choice-Name": {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True
        }
    '''
    return_val = None
    if isinstance(data, dict):        
        first_key = next(iter(data))
        if first_key:
            data_content = data.get(first_key)
            if isinstance(data_content, dict):
                return_val = data_content
                
    return return_val

def get_j_field(j_field_list, data_key, is_using_ids):
    j_field_found = None
    
    for j_field in j_field_list:
        if is_using_ids:
            if j_field[0] == int(data_key):
                j_field_found = j_field
                break
        else:
            if j_field[1] == data_key:
                j_field_found = j_field
                break
            
    return j_field_found             
        

def get_map_of_data_content(data: dict):
    '''
    MapOf Data Example:
        {
            "Root-Test": [1, "asdf", 2, "fdsaf"]
        }
    '''
    return_val = None
    if isinstance(data, dict):        
        first_key = next(iter(data))
        if first_key:
            data_content = data.get(first_key)
            if isinstance(data_content, list):
                return_val = data_content
            elif isinstance(data_content, dict):
                return_val = data_content
                
    return return_val

def get_nested_value(data, keys, default=None):
    """
    Safely retrieves a value from a nested dictionary given a list of keys.

    Args:
        data (dict): The dictionary to search within.
        keys (list): A list of keys representing the path to the desired value.
        default: The value to return if the key path doesn't exist. Defaults to None.

    Returns:
        The value at the specified path or the default value if not found.
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def get_reference_type(jschema, type_name):
    j_types = jschema.get('types')
    ref_type = get_schema_type_by_name(j_types, type_name)
    if not ref_type:
        raise ValueError(f"Unknown type {type_name} referenced" )
    return ref_type

def get_schema_type_by_name(j_types: list, name: str):
    type_list = [j_type for j_type in j_types if j_type[0] == name]
    type = None
    
    if type_list == None or get_item_safe_check(type_list, 0) == None:
        return None
    else:
        type = get_item_safe_check(type_list, 0)
    
    return type

def get_schema_types(j_types: list, base_type: str):
    return [j_type for j_type in j_types if j_type[1] == base_type]

def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return n % 2 != 0

def is_enumerated(jadn_type: list[any]):
    if len(jadn_type) == 3:
            return True
    return False

def is_field(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], int):
            return True
    return False

def is_type(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], str):
            return True
    return False

def safe_get(lst, index, default=None):
    """Safely get an item from a list at a given index.

    Args:
        lst: The list to access.
        index: The index to retrieve.
        default: The value to return if the index is out of range.

    Returns:
        The item at the given index, or the default value if the index is out of range.
    """
    try:
        return lst[index]
    except IndexError:
        return default
    
def search_string(regex_pattern, text):
  """Searches a string for the regex pattern and returns the result."""
  if regex_pattern:
    match = regex_pattern.search(text)
    if match:
      return match.group()
    else:
      return None
  return None    

def split_on_first_char(string):
    """Splits a string on the first character."""

    if not string:
        return []

    return [string[0], string[1:]]

def split_on_second_char(string):
    """Splits a string on the second character."""

    if not string:
        return []

    return [string[:2], string[2:]]

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
