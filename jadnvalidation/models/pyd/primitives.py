from __future__ import annotations
import re

from functools import partial
from typing import Any
from pydantic import BaseModel


def get_max_len(cls) -> int:
    # TODO: Need to fill in... 
    
    # config = Config()
    # if cls.__options__.maxv is None:
    #     try:
    #         maxProps = cls.__config__.info.get('$MaxString')
    #     except AttributeError:
    #         maxProps = config.MaxElements
    #         pass   
    # else:
    #     maxProps = cls.__options__.maxv or config.MaxElements
        
    maxProps = 255
    return int(maxProps)

# def validate_format(cls: DefinitionBase, fmt: str, val: Any) -> Any:
def validate_format(cls: BaseModel, fmt: str, val: Any) -> Any:
    """
    Attempt to validate the format of a given Primitive type
    :param cls: Primitive type to validate
    :param fmt: format to validate against
    :param val: value to validate
    :raise Exception: invalid format
    :return: original formatted value
    """
    
    # We might be able to use our new options logic for strings here
    
    if re.match(r"^u\d+$", fmt):
        fun = partial(cls.__options__.validation["unsigned"], int(fmt[1:]))
    else:
        fun = cls.__options__.validation.get(fmt, None)

    if fun:
        return fun(val)
    raise ValueError(f"{fmt} is not a valid format")

# TODO: May not be needed
class Integer(int):
    
    @classmethod
    def __init__(self, **data):
        hit = ""    
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: any, values):
        if type(value) is not int:
            raise ValueError("Invalid integer")
        
        return value

class String(str):
    
    __test: str = "test"
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        return value