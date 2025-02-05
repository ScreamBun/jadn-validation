from pydantic import BaseModel, ConfigDict, model_validator

from jadnvalidation.utils.general_utils import all_unique, get_global_configs, get_type_opts


class Choice(BaseModel):
    """
    A discriminated union: one type selected from a set of named or labeled types.
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
        Pydantic validator - validate the data as a Choice type
        :param value: data to validate
        :raise ValueError: invalid data given
        :return: original data
        """
        
        global_configs = get_global_configs(cls)
        type_opts = get_type_opts(cls)
        
        if global_configs and global_configs.MaxElements:
            max_elements = global_configs.MaxElements
            
            if value and isinstance(value, dict):
                for item in value.values():
                    if isinstance(item, dict):
                        if len(item) > max_elements:
                            raise ValueError(f"Max Number of elements ({max_elements}) exceeded")
                    break
        
        model_fields = cls.model_fields
        model_fields_len = len(model_fields)
        
        if value and isinstance(value, dict):
            data_keys = value.keys()
            data_keys_len = len(data_keys)
            
            if type_opts and type_opts.use_field_id:
                # If using field id, then all ids should be integers and unique
                try:
                   int_list = [int(x) for x in data_keys] 
                except:
                    raise ValueError(f"Choice option key/id must be an integer")
                
                try:
                    if not all_unique(data_keys):
                        raise ValueError(f"All Choice option keys/ids must be unique")
                except:
                    raise ValueError(f"Unable to check Choice option keys/ids for uniqueness")                
                                
            # Choice data cannot exceed the number choice options
            if data_keys_len > model_fields_len:
                raise ValueError(f"Choice options cannot exceed {model_fields_len} options")
            
            # Choice data must be a choice option
            model_field_keys = model_fields.keys()
            for data_key in data_keys:
                if data_key not in model_field_keys:
                    raise ValueError(f"Choice option '{data_key}' not found")

        return value