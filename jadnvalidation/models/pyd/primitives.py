from __future__ import annotations
import re

from functools import partial
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, model_validator


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

class Integer(int):
    
    # min: int = 0
    # max: int = 5
    
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
        
        # value_int = int(value_int)
        # if cls.min < value_int:
        #     raise ValueError("Integer less than " + cls.min)
        # if cls.max > value_int:
        #     raise ValueError("Integer greater than " + cls.max)
        
        return value

# Works
class String(str):

    @classmethod
    def __init__(self, **data):
        hit = ""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: any, values):
        if not isinstance(value, str):
            raise ValueError("Invalid string")
        return value



class TitleCaseStr(str):
    model_config = ConfigDict(arbitrary_types_allowed = True)
    
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate    
        
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = None
        if not m:
            raise ValueError('invalid postcode format')
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        # return cls(f'{m.group(1)} {m.group(2)}')        
        return cls    
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        pass       
    
    def __new__(cls, value: str):
        return super().__new__(cls, value.title()) 


# Inhiert from Pydantic str
class StringOld(BaseModel): 
    # root: str
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra='allow')

    def __init__(self, **kwargs):
        hit = ""

    @model_validator(mode="before") 
    def validate_data(cls, value: str) -> str:  # pylint: disable=no-self-argument
        """
        Pydantic validator - validate the string as a String type
        :param value: value to validate
        :raise ValueError: invalid data given
        :return: original value
        """
        # val = value.get(cls.root, None)
        # if fmt := cls.__options__.format:
        #     validate_format(cls, fmt, val) 
        # val_len = len(val)
        # min_len = cls.__options__.minv or 0
        # max_len = get_max_len(cls)
        # if min_len > val_len:
        #     raise ValueError(f"{cls.name} is invalid, minimum length of {min_len} characters not met")
        # if max_len < val_len:
        #     raise ValueError(f"{cls.name} is invalid, maximum length of {max_len} characters exceeded")
        return value

    
# class CustomStr(str):
#     """Custom string class that adds a prefix to the string"""
#     model_config = ConfigDict(arbitrary_types_allowed = True)
#     # def __new__(cls, value):
#     #     return super().__new__(cls, f"custom_{value}")
    
#     # @classmethod
#     # def __get_pydantic_core_schema__(cls, source, handler):
#     #     pass 
#     @model_validator(mode='before')
#     def validate_data(cls, value: dict) -> dict:
#         test = ""