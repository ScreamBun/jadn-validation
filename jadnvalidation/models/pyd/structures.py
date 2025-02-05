from __future__ import annotations
from random import randint
from pydantic import BaseModel, ConfigDict, model_validator

from jadnvalidation.models.jadn.jadn_config import DEFAULT_MAX_ELEMENTS, MAX_ELEMENTS_KEY
from jadnvalidation.utils.general_utils import get_global_configs, get_type_opts
from jadnvalidation.utils.mapping_utils import get_min_max

def validate_min_max_items(value, min, max):
    if min or max:
        if value and isinstance(value, dict):
            # for item in value.values():
                if isinstance(value, dict):
                    if min and len(value.values()) < min:
                        raise ValueError(f"Min Number of elements ({min}) required")                    
                    if max and len(value.values()) > max:
                        raise ValueError(f"Max Number of elements ({max}) exceeded")
                # break    

# TODO: Change to BaseModel
class Array(list):
    """
    An ordered list of labeled fields with positionally-defined semantics. 
    Each field has a position, label, and type.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: any, values):
        if not isinstance(value, list):
            raise ValueError("Invalid list")    
        return value
    
class Map(BaseModel):
    """
    An unordered map from a set of specified keys to values with semantics bound to each key. 
    Each key has an id and name or label, and is mapped to a value type.
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
        Map Custom Rules:
        - An instance of a Map, MapOf, or Record type MUST NOT have more than one occurrence of each key.
        - An instance of a Map, MapOf, or Record type MUST NOT have a key of the null type.
        - An instance of a Map, MapOf, or Record type with a key mapped to a null value MUST compare as equal 
          to an otherwise identical instance without that key.
        """
        
        global_configs = get_global_configs(cls)
        type_opts = get_type_opts(cls)
        model_fields = cls.model_fields
        model_fields_len = len(model_fields)        
        
        if global_configs and global_configs.MaxElements:
            max_elements = global_configs.MaxElements
            
            if value and isinstance(value, dict):
                for item in value.values():
                    if isinstance(item, dict):
                        if len(item) > max_elements:
                            raise ValueError(f"Max Number of elements ({max_elements}) exceeded")
                    break
                
        if value and isinstance(value, dict):
            data_keys = value.keys()
            data_keys_len = len(data_keys)
            
            # Map data cannot exceed the number of mappings, unless extends is selected
            if data_keys_len > model_fields_len:
                raise ValueError(f"Choice options cannot exceed {model_fields_len} options")
            
            # Map data must be a mapping
            model_field_keys = model_fields.keys()
            for data_key in data_keys:
                if data_key not in model_field_keys:
                    raise ValueError(f"Choice option '{data_key}' not found")                

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
        
        global_configs = get_global_configs(cls)
        type_opts = get_type_opts(cls)
        
        # Min / Max Elements Validation
        min, max = get_min_max(global_configs, type_opts)
        validate_min_max_items(value, min, max)

        return value 