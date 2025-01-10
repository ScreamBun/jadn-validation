from __future__ import annotations
from random import randint
from pydantic import BaseModel, ConfigDict, model_validator

# TODO: Change to BaseModel
class Array(list):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: any, values):
        if not isinstance(value, list):
            raise ValueError("Invalid list")    
        return value
      

class Record(BaseModel):
    """
    An ordered map from a list of keys with positions to values with positionally-defined semantics.
    Each key has a position and name, and is mapped to a value type. Represents a row in a spreadsheet or database table.
    """ 
    
    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='allow')
 
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