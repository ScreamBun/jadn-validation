from __future__ import annotations
from collections import namedtuple
import re
import sys
from typing import Any, Callable, Dict, Set, Type, Union, get_args
from pydantic import BaseModel, Field, create_model

from jadnvalidation.models.pyd.primitives import String
from jadnvalidation.models.pyd.structures import Record
from jadnvalidation.pydantic_schema import build_jadn_type_obj


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

def make_def(data: list, formats: Dict[str, Callable] = None) -> Type[Definition]:
    """
    Create a custom definition with the given arguments
    :param data: the original JADN for the definition
    :param formats: the JADN format validators
    :return: type definition class
    """
    j_type_def = jadn_def(*data)
    if cls := DefTypes.get(j_type_def.type):
        cls_kwargs = {}
        p_fields = {}
        
        for j_field in j_type_def.fields:

            # field_obj["options"] = Options(field_obj["options"], name=f"{def_obj.type_name}.{name}", data_type=field_obj.get("type", "String"), validation=formats)
            
            field_obj = dict(def_field(*j_field)._asdict()) # Note: Pydantic needs fields to be mapped values
            field_name = field_obj["name"]
            field_type = field_obj["type"]
            
            p_fields[field_name] = (field_type, Field(description='foo description', alias=field_name))
        
        alias = clsName(j_type_def.name)
        
        # TODO: What are these used for?
        # Warning: In Pydantic V2, the __init_subclass__() method for BaseModel was changed and no longer accepts keyword arguments.
        # cls_kwargs.update(
        #     __name__= alias,
        #     __doc__= j_type_def.description,
        #     __options__=Options(j_type_def.options, name=j_type_def.name, validation=formats)
        # )
        
        # def_model = create_model(j_type_def.name, __base__=cls, __cls_kwargs__=cls_kwargs, **p_fields)
        def_model = create_model(j_type_def.name, **p_fields)
        # Student_User2 = pydantic.create_model("Student_User2", __base__=type("_UserStudentBase", (User, Student), {}))    
        # def_model = create_model(j_type_def.name, **p_fields)
        
        return def_model
    
    raise TypeError(f"Unknown definition of {j_type_def.type}")


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def update_types(j_types: list) -> dict:
    pd_schema_types = {}
    
    # 1) Iterate over types....
    for j_type in j_types:
        j_type_obj = build_jadn_type_obj(j_type)
    
        # 2) Add fields to the model if there are any (only structures will contain fields)
        p_fields = {}
        for j_field in j_type_obj.fields:
            field_obj = dict(def_field(*j_field)._asdict()) # Note: Pydantic needs fields to be mapped values
            field_name = field_obj["name"]
            field_type = field_obj["type"]
            # field_type_cls = clsName(field_type)
            field_type_cls = DefTypes.get(field_type)
            p_fields[field_name] = (field_type_cls, Field(description='foo description', alias=field_name))            
            
        # 3) Create new model w/ fields
        pd_type_cls = DefTypes.get(j_type_obj.base_type)
        # pd_type_cls_2 = str_to_class(j_type_obj.base_type)
        type_name_cls = clsName(j_type_obj.type_name)
        pd_type_model = create_model(type_name_cls, __base__=pd_type_cls, **p_fields)
        
        # 4) Add to list of models
        pd_schema_types[j_type_obj.type_name] = pd_type_model
        
    # 5) Add base models - Not sure what this is doing yet....
    # pd_schema_types.update(DefTypes)
    # for def_cls in pd_schema_types.values():
    #     try:
    #         # def_cls.update_forward_refs(**cls_defs) 
    #         def_cls.model_rebuild(**cls_defs)
    #     except Exception as err:
    #         # Schema is unresolved
    #         if namespace and err.name.split('__')[0] in namespace:
    #            continue
    #         else:
    #             raise Exception(err) 
    
    # cls_defs = {d.__name__: d for d in pd_schema_types.values()}
    # cls_defs.update(DefTypes)
    # for def_cls in pd_schema_types.values():
    #     try:
    #         # def_cls.update_forward_refs(**cls_defs) 
    #         def_cls.model_rebuild(**cls_defs)
    #     except Exception as err:
    #         # Schema is unresolved
    #         # if namespace and err.name.split('__')[0] in namespace:
    #         #    continue
    #         # else:
    #             raise Exception(err)    
    
    # for pd_type_md in pd_schema_types.values():
    #     pd_type_md.model_rebuild()
    
    return pd_schema_types
    


def update_types_old(types: Union[dict, list], formats: Dict[str, Callable] = None, namespace: Set = None) -> dict:
    if isinstance(types, list):
        def_types = {td[0]: make_def(td, formats) for td in types}
        # cls_defs = {d.__name__: d for d in def_types.values()}
        # cls_defs.update(DefTypes)
        # for def_cls in def_types.values():
        #     try:
        #         # def_cls.update_forward_refs(**cls_defs) 
        #         def_cls.model_rebuild(**cls_defs)
        #     except Exception as err:
        #         # Schema is unresolved
        #         if namespace and err.name.split('__')[0] in namespace:
        #            continue
        #         else:
        #             raise Exception(err)
        return def_types
    return types


class DynamicModel(BaseModel):
    name: str
    value: int

class Schema(BaseModel):
    # info: Optional[Information] = Field(default_factory=Information)
    types: dict = Field(default_factory=dict) 
    
    def __init__(self, **kwargs):
        if "types" in kwargs:
            kwargs["types"] = update_types(kwargs["types"])
        super().__init__(**kwargs)
        hit = ""
        # nms = None
        # if "types" in kwargs:
        #     kwargs["types"] = update_types(kwargs["types"], self.__formats__, nms)
        # super().__init__(**kwargs)
        # DefinitionBase.__config__.types = self.types    
        
    # def model_post_init(self, __context):
    #     # types = update_types(types)
    #     hit = ""