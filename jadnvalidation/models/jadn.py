from typing import Tuple
from pydantic import BaseModel, Field, HttpUrl


class Config(BaseModel):
    max_binary: int = Field(alias='$MaxBinary', default=255) 
    max_string: int = Field(alias='$MaxString', default=255) 
    max_elements: int = Field(alias='$MaxElements', default=100) 
    sys: str = Field(alias='$Sys', default='$') 
    type_name: str = Field(alias='$TypeName', default='^[A-Z][-$A-Za-z0-9]{0,63}$') 
    field_name: str = Field(alias='$FieldName', default='^[a-z][_A-Za-z0-9]{0,63}$') 
    nsid: str = Field(alias='$NSID', default='^[A-Za-z][A-Za-z0-9]{0,7}$') 

class Info(BaseModel):
    package: HttpUrl
    version: str | None = None
    title: str | None = None
    description: str | None = None
    comment: str | None = None
    copyright: str | None = None
    license: str | None = None
    exports: list[str] = None
    namespaces: dict[str, str] = None
    config: Config | None = None

class Jadn(BaseModel):
    info: Info | None = None