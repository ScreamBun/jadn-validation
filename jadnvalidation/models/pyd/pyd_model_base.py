from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, ValidationInfo, model_validator

from jadnvalidation.consts import DYNAMIC_MODEL
from jadnvalidation.models.jadn.jadn_type import Base_Type


class SBBaseModel(BaseModel):
    
    # model_config = ConfigDict(
    #     from_attributes=True, 
    #     allow_mutation=True
    #     ) 
    
    minv: Optional[int] = None
    maxv: Optional[int] = None
    jadn_type: Optional[str] = None
    
    @model_validator(mode='after')
    @classmethod
    def validate_model(cls, data: Any, info: ValidationInfo) -> Any:

        title = info.config["title"]
        if DYNAMIC_MODEL == title:
            
            a = cls.model_fields["jadn_type"] 
            
            if cls.model_fields["jadn_type"] == Base_Type.RECORD.value:
            
                if cls.minv and cls.minv > len(data):
                    if cls.minv == 1:
                        raise ValueError("A minimum of {cls.minv} field is required.")
                    else:
                        raise ValueError("A minimum of {cls.minv} fields are required.")
                
                if cls.maxv and cls.maxv > len(data):
                    if cls.maxv == 1:
                        raise ValueError("A maximum of {cls.maxv} field is required.")                
                    else:
                        raise ValueError("A maximum of {cls.maxv} fields are required.")                    
        
        return data 

    # @model_validator(mode='after')
    # def validate_record(self):
    #     hit = ""
    #     # pw1 = self.password1
    #     # pw2 = self.password2
    #     # if pw1 is not None and pw2 is not None and pw1 != pw2:
    #     #     raise ValueError('passwords do not match')
    #     return self    