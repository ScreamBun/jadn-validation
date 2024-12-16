from pydantic import BaseModel, ConfigDict, RootModel, field_validator, model_validator, validator

from jadnvalidation.models.pyd.options import Options

def get_max_v(cls) -> int:
    # TODO: Need to fill in... 
    
    # config = Config()
    # if cls.__options__.maxv is None:
    #     try:
    #         maxProps = cls.__config__.info.get('$MaxElements')
    #     except AttributeError:
    #         maxProps = config.MaxElements
    #         pass   
    # else:
    #     maxProps = cls.__options__.maxv or config.MaxElements
        
    maxProps = 255        
    return int(maxProps)


class Record(BaseModel):
    """
    An ordered map from a list of keys with positions to values with positionally-defined semantics.
    Each key has a position and name, and is mapped to a value type. Represents a row in a spreadsheet or database table.
    """ 
    
    model_config = ConfigDict(from_attributes=True)     
    
    # __root__: dict
    __options__ = Options(data_type="Record") 
    
    @field_validator("*")
    def check_range(cls, v):
        if v:     
            test = ""
 
    @model_validator(mode='before')
    def validate_data(cls, value: dict) -> dict:
        """
        Pydantic validator - validate the data as a Record type
        :param value: data to validate
        :raise ValueError: invalid data given
        :return: original data
        """
                
        minProps = cls.__options__.minv or 0
        maxProps = get_max_v(cls)

        if len(value) < minProps: 
            raise ValueError("minimum property count not met")

        if len(value) > maxProps:
            raise ValueError("maximum property count exceeded")

        return value

    # class Config:
    #     extra = Extra.forbid

    class Options:
        data_type = "Record"