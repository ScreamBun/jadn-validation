import sys
from typing import Callable, Union
from pydantic import BaseModel, Field, create_model
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

def create_dynamic_model(model_name: str, fields: dict) -> type[BaseModel]:
    return create_model(
        model_name,
        **fields
    )

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
    return data.get(name)

def get_global_configs(p_model):
    global_configs = None
    if p_model.model_fields:
        gc_field_info = p_model.model_fields.get(ROOT_GLOBAL_CONFIG_KEY, None)
        if not gc_field_info:
            gc_field_info = p_model.model_fields.get(GLOBAL_CONFIG_KEY, None)
        if gc_field_info and gc_field_info.default:
            global_configs = gc_field_info.default
                
    return global_configs

def get_jadn_type_opts(jadn_type_name: str) -> tuple:
    return ALLOWED_TYPE_OPTIONS.get(jadn_type_name)

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
