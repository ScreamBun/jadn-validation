import sys
import importlib

from typing import Callable, Union
#from pydantic import BaseModel, create_model
from consts import ALLOWED_TYPE_OPTIONS
from jadnvalidation.models.jadn.jadn_config import GLOBAL_CONFIG_KEY, ROOT_GLOBAL_CONFIG_KEY, TYPE_OPTS_KEY
from jadnvalidation.models.pyd.pyd_field_mapper import Pyd_Field_Mapper

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

def create_derived_class(base_class, class_name, extra_methods=None):
    """
    Dynamically creates a new class inheriting from base_class.

    Args:
        base_class: The class to inherit from.
        class_name: The name of the new class.
        extra_methods: A dictionary of additional methods for the new class.

    Returns:
        The newly created class.
    """
    if extra_methods is None:
        extra_methods = {}
    return type(class_name, (base_class,), extra_methods)

""" - removing in the shift from pydantic KC
def create_dynamic_model(model_name: str, fields: dict) -> type[BaseModel]:
    return create_model(
        model_name,
        **fields
    )
    """
    
# (class_name, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None)
def create_clz_instance(class_name: str, *args, **kwargs):
    modules = {
        "Array" : "jadnvalidation.data_validation.array",
        "ArrayOf" : "jadnvalidation.data_validation.array_of",
        "Binary" : "jadnvalidation.data_validation.binary",
        "Boolean" : "jadnvalidation.data_validation.boolean",
        "Integer" : "jadnvalidation.data_validation.integer",
        "Record" : "jadnvalidation.data_validation.record",
        "String" : "jadnvalidation.data_validation.string"
    }

    module = importlib.import_module(modules.get(class_name))
    cls = getattr(module, class_name)
    
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

def get_data_by_name(data: dict, name: str):
    # TODO: If not found, perhaps return data as-is?
    
    # if isinstance(data, dict):
    #     if target_key in data:
    #         return data[target_key]
    #     for value in data.values():
    #         result = get_data_by_name(value, target_key)
    #         if result is not None:
    #             return result
    # elif isinstance(data, list):
    #     for item in data:
    #         result = get_data_by_name(item, target_key)
    #         if result is not None:
    #             return result
    
    return data.get(name)
    # return None

def get_global_configs(p_model):
    global_configs = None
    if p_model.model_fields:
        gc_field_info = p_model.model_fields.get(ROOT_GLOBAL_CONFIG_KEY, None)
        if not gc_field_info:
            gc_field_info = p_model.model_fields.get(GLOBAL_CONFIG_KEY, None)
        if gc_field_info and gc_field_info.default:
            global_configs = gc_field_info.default
                
    return global_configs

def get_item_safe_check(my_list, index):
    if 0 <= index < len(my_list):
        return my_list[index]
    return None  # Or any other default value

def get_jadn_type_opts(jadn_type_name: str) -> tuple:
    return ALLOWED_TYPE_OPTIONS.get(jadn_type_name)

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

def get_type_opts(p_model) -> Pyd_Field_Mapper:
    opts = None
    if p_model.model_fields:
        type_opts_field = p_model.model_fields.get(TYPE_OPTS_KEY, None)
        if type_opts_field and type_opts_field.default:
            opts = type_opts_field.default
                
    return opts

def is_type(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], str):
            return True
    return False

def is_field(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], int):
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

class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super().__get__(objtype)

    def __set__(self, obj, value):
        super().__set__(type(obj), value)

    def __delete__(self, obj):
        super().__delete__(type(obj))
