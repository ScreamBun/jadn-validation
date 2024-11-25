from typing import Self
from pydantic import BaseModel, model_validator


class Record(BaseModel):
    # __options__ = Options(data_type="Record")

    @model_validator(mode='before')
    def validate_data(cls, value: dict) -> dict:
        print('after validator running custom validation...')
        return cls
    
    class Options:
        data_type = "Record"
