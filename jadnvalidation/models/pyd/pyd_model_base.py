from typing import Any
from pydantic import BaseModel, ValidationInfo, model_validator


class SBBaseModel(BaseModel):
    minv: int = None
    maxv: int = None
    
    @model_validator(mode='after')
    @classmethod
    def validate_record(cls, data: Any, info: ValidationInfo) -> Any:
        hit = ""
        # if isinstance(data, dict):
        #     assert (
        #         'card_number' not in data
        #     ), 'card_number should not be included'
        return data 

    # @model_validator(mode='after')
    # def validate_record(self):
    #     hit = ""
    #     # pw1 = self.password1
    #     # pw2 = self.password2
    #     # if pw1 is not None and pw2 is not None and pw1 != pw2:
    #     #     raise ValueError('passwords do not match')
    #     return self    