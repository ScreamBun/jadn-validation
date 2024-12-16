from collections import namedtuple
import re
from typing import Annotated, Any, Callable, ClassVar, Dict, Optional, Set, Type, Union, get_args
from pydantic import BaseModel, Field, create_model

from jadnvalidation.models.pyd.options import Options
from jadnvalidation.models.pyd.primitives.string import String
from jadnvalidation.models.pyd.structures import ValidationFormats
from jadnvalidation.models.pyd.structures.record import Record
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
        
        # TODO: Special logic for Enumerations?
        # if def_obj.type == "Enumerated":
        #     values = {}
        #     for field in def_obj.fields:
        #         field_obj = dict(enum_field(*field)._asdict())
        #         field_obj["default"] = field_obj["name"]
        #         values[field_obj.pop("name")] = Field(**field_obj)
        #     cls_kwargs["__enums__"] = Enum("__enums__", values)
        # else:
        
        for j_field in j_type_def.fields:

            # field_obj["options"] = Options(field_obj["options"], name=f"{def_obj.type_name}.{name}", data_type=field_obj.get("type", "String"), validation=formats)
            
            field_obj = dict(def_field(*j_field)._asdict()) # Note: Pydantic needs fields to be mapped values
            field_name = field_obj["name"]
            field_type = field_obj["type"]
            field_obj["options"] = Options(field_obj["options"], name=f"{j_type_def.name}.{field_name}", data_type=field_type, validation=formats)

            # TODO: Add alias name logic            
            # if alias := FieldAlias.get(name):
            #     field_obj["alias"] = name
            #     name = alias
            
            # field_cls_type = clsName(field_obj.get("type", "String"))
            if j_type_def.type == "Choice" or field_obj["options"].isOptional():
                # annotation = Optional[field_cls_type]
                annotation = Optional[field_type]
                field_obj["required"] = False
            else:
                # annotation = field_cls_type
                annotation = field_type
                field_obj["required"] = True
            
            # p_field_info = Field(**field_obj)
            # p_field_info = (String, None)
            # p_fields[field_name] = (annotation, p_field_info)
            
            # field_info = Field(**field_obj)
            p_fields[field_name] = (field_type, Field(description='foo description', alias=field_name))
            # p_fields[field_name] = (String, ...)
        
        alias = clsName(j_type_def.name)
        # alias = ClassVar(j_type_def.type)
        # alias2 = SysAlias.sub("__", j_type_def.name)
        
        # TODO: What are these used for?
        # Warning: In Pydantic V2, the __init_subclass__() method for BaseModel was changed and no longer accepts keyword arguments.
        cls_kwargs.update(
            __name__= alias,
            __doc__= j_type_def.description,
            __options__=Options(j_type_def.options, name=j_type_def.name, validation=formats)
        )
        
        # def_model = create_model(j_type_def.name, __base__=cls, __cls_kwargs__=cls_kwargs, **p_fields)
        # def_model = create_model(j_type_def.name, __base__=cls, **p_fields)
        def_model = create_model(j_type_def.name, **p_fields)
        
        return def_model
    
    raise TypeError(f"Unknown definition of {j_type_def.type}")


def update_types(types: Union[dict, list], formats: Dict[str, Callable] = None, namespace: Set = None) -> dict:
    if isinstance(types, list):
        def_types = {td[0]: make_def(td, formats) for td in types}
        # cls_defs = {d.__name__: d for d in def_types.values()}
        # cls_defs.update(DefTypes)
        # for def_cls in def_types.values():
        #     try:
        #         def_cls.update_forward_refs(**cls_defs)
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
    # types: dict = Field(default_factory=dict)
    # types: Dict[str, Any]
    # types: dict = Field(default_factory=dict) 
    types: dict = Dict[str, DynamicModel]
    __formats__: Dict[str, Callable] = ValidationFormats
    
    def __init__(self, **kwargs):
        # TODO: Uncomment once we are ready for namespaces
        # if "info" in kwargs and "namespaces" in kwargs["info"]:
        #     nms = set(kwargs["info"]["namespaces"])
        # else: 
        #     nms = None
        
        # TODO: This is how configs make it into Def Base....
        # if "info" in kwargs and "config" in kwargs["info"]:
        #     DefinitionBase.__config__.info = kwargs["info"]["config"]
    
        nms = None
        if "types" in kwargs:
            kwargs["types"] = update_types(kwargs["types"], self.__formats__, nms)
        super().__init__(**kwargs)
        # DefinitionBase.__config__.types = self.types    