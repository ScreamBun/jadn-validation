from __future__ import annotations
from collections import namedtuple
import re
import sys
from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, Type, Union, get_args
from pydantic import BaseModel, Field, create_model

from jadnvalidation.models.pyd.primitives import String, Integer
from jadnvalidation.models.pyd.structures import Record, Array
from jadnvalidation.pydantic_schema import build_custom_model, build_jadn_type_obj, build_pyd_field


# Primitive = Union[Binary, Boolean, Integer, Number, String]
Primitive = Union[String]
# Structure = Union[Array, ArrayOf, Choice, Enumerated, Map, MapOf, Record]
Structure = Union[Record]
Definition = Union[Primitive, Structure]
# DerivedArg = Union[
#     Type[Union[ArrayOf, MapOf]],
#     Dict[str, Tuple[str, FieldInfo]]
# ]
DefTypes = {d.__name__: d for d in get_args(Definition)}
jadn_def = namedtuple("jadn_def", ("name", "type", "options", "description", "fields"), defaults=(None, None, [], "", []))
def_field = namedtuple("def_field", ("id", "name", "type", "options", "description"))

ValidName = re.compile(r"^[A-Za-z_][A-Za-z0-9_]_")
SysAlias = re.compile(r"[:$?&|!{}\[\]()^~*\"'+\-\s]")

def clsName(name: str) -> str:
    if ValidName.match(name):
        return name
    return SysAlias.sub("__", name)


def build_custom_models(j_types: list, j_config = None) -> type[BaseModel]:
    """
    Creates a Pydantic models dynamically based on a list of JADN Types.
    Return a dictionary of models
    """

    p_models_dict = {}
    for j_type in j_types:
        j_type_obj = build_jadn_type_obj(j_type)
            
        if j_type_obj:
            
            p_fields = {}
            for j_field in j_type_obj.fields: 
                j_field_obj = build_jadn_type_obj(j_field)
                p_field = build_pyd_field(j_field_obj)
                p_fields[j_field_obj.type_name] = p_field
                
            # TODO: Create add these to build_pyd_field or their own functions
            # TODO: See l_config for global_opts
            p_fields["type_opts"] = (str, Field(default="testing model opts", exclude=True, evaluate=False))
            p_fields["global_opts"] = (str, Field(default="testing global opts", exclude=True, evaluate=False))
    
            p_models_dict[j_type_obj.type_name] = create_model(j_type_obj.type_name, __base__=Record, **p_fields)
    
    return p_models_dict

class Schema(BaseModel):
    # info: Optional[Information] = Field(default_factory=Information)
    types: dict = Field(default_factory=dict) 
    
    def __init__(self, **kwargs):
        if "types" in kwargs:
            
            j_config = []
            j_types = []
            if kwargs["info"]["config"]:
                j_config = kwargs["info"]["config"]
                
            if kwargs["types"]:
                j_types = kwargs["types"]
                custom_model = build_custom_models(j_types, j_config)
            else:
                raise ValueError("Types missing from JADN Schema")            
            
            kwargs["types"] = update_types(kwargs["types"])
        super().__init__(**kwargs)