import re

from functools import partial
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator, model_validator

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


# class String(RootModel[str]): 
class String(str): 
    """
    A sequence of characters, each of which has a Unicode codepoint. Length is the number of characters.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed = True
    )    
    
    # __root__: str = Field(..., alias="__root__")
    __options__ = Options(data_type="String")  # pylint: disable=used-before-assignment

    # Validation
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        # Add your custom validation logic here
        return cls(value)        
    
    
    @model_validator(mode='before')
    def validate_data(cls, value: dict) -> dict:  # pylint: disable=no-self-argument
        """
        Pydantic validator - validate the string as a String type
        :param value: value to validate
        :raise ValueError: invalid data given
        :return: original value
        """
        val = value.get("__root__", None)
        if fmt := cls.__options__.format:
            validate_format(cls, fmt, val)
        val_len = len(val)
        min_len = cls.__options__.minv or 0
        max_len = get_max_len(cls)
        if min_len > val_len:
            raise ValueError(f"{cls.name} is invalid, minimum length of {min_len} characters not met")
        if max_len < val_len:
            raise ValueError(f"{cls.name} is invalid, maximum length of {max_len} characters exceeded")
        return value

    # class Config:
    #     arbitrary_types_allowed = True

    class Options:
        data_type = "String"