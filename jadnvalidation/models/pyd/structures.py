from __future__ import annotations
from pydantic import BaseModel, ConfigDict, model_validator


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
    def __init__(self, **data):
        hit = "" 
    
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
    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra='allow')
    # __options__ = Options(data_type="Record") 
    
    def __init__(self, **data):
        hit = ""
 
    @model_validator(mode='before')
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
        
        if not isinstance(value, list):
            raise ValueError("Invalid record")        

        return value

    # class Config:
    #     extra = Extra.forbid

    # class Options:
    #     data_type = "Record"