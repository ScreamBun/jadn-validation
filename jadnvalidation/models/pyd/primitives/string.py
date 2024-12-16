import re

from functools import partial
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, GetCoreSchemaHandler, RootModel, field_validator, model_validator
from pydantic_core import CoreSchema, core_schema

from jadnvalidation.models.pyd.options import Options


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


def fn(v: str) -> str:
    assert 'hello' in v
    return v + 'world'


# Inhiert from Pydantic str
class String(str): 
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed = True)
    junk: str = Field(exclude=True)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.chain_schema(
            [
                core_schema.str_schema(strict=True),
                core_schema.no_info_plain_validator_function(function=fn)
            ]
        )
        

    
class CustomStr(str):
    """Custom string class that adds a prefix to the string"""
    model_config = ConfigDict(arbitrary_types_allowed = True)
    # def __new__(cls, value):
    #     return super().__new__(cls, f"custom_{value}")
    
    # @classmethod
    # def __get_pydantic_core_schema__(cls, source, handler):
    #     pass 
    @model_validator(mode='before')
    def validate_data(cls, value: dict) -> dict:
        test = ""