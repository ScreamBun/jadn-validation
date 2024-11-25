from typing import Self
from pydantic import BaseModel, model_validator


class ModelDict(BaseModel):
    # __options__ = Options(data_type="Record")

    @model_validator(mode='before')
    def validate_before(self: Self) -> Self:
        print('after validator running custom validation...')
        return self
