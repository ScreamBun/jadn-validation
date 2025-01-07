from __future__ import annotations
from random import randint
from typing import ClassVar, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator


class Array(list):
    
    @classmethod
    def __init__(self, **data):
        hit = "" 
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: any, values):
        if not isinstance(value, list):
            raise ValueError("Invalid list")    
        return value
    
    
class Record(dict):    
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: any, values):
        if not isinstance(value, dict):
            raise ValueError("Invalid record")
        
        # TODO: Check that all keys are str, check legacy code for more detailed validations for records

        return value    

class RecordOld(BaseModel):
    """
    An ordered map from a list of keys with positions to values with positionally-defined semantics.
    Each key has a position and name, and is mapped to a value type. Represents a row in a spreadsheet or database table.
    """ 
    
    _secret_value: str = PrivateAttr()
        
    # def __init_subclass__(cls, opts: Optional[str] = None):
    #     cls._opts[type or cls.__name__.lower()] = cls      
    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra='allow')
    # __options__ = Options(data_type="Record") 
    
    # def __init__(self, **data):
    #     hit = ""
 
    # @classmethod
    # def __pydantic_validator__(cls, v, field, config):
    #     if field.name == "name":
    #         if not v.isalpha():
    #             raise ValueError("Name must only contain letters")
    #     return v
    
    def __init__(self, **data):
        super().__init__(**data)
        # this could also be done with default_factory
        self._secret_value = randint(1, 5)     
 
    @model_validator(mode='before')
    @classmethod
    def validate_data(cls, value: any) -> dict:
        """
        Pydantic validator - validate the data as a Record type
        :param value: data to validate
        :raise ValueError: invalid data given
        :return: original data
        """
                
        # minProps = cls.__options__.minv or 0
        # maxProps = get_max_v(cls)

        # if len(value) < minProps: 
        #     raise ValueError("minimum property count not met")

        # if len(value) > maxProps:
        #     raise ValueError("maximum property count exceeded")
        
        # if not isinstance(value, list):
        #     raise ValueError("Invalid record")        

        return value
    
    # @model_validator(mode='wrap')
    # @classmethod
    # def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Any]) -> Any:
    #     try:
    #         return handler(data)
    #     except ValidationError:
    #         logging.error('Model %s failed to validate with data %s', cls, data)
    #         raise    