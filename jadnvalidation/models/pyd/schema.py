from __future__ import annotations
from collections import namedtuple
import re
import sys
from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, Type, Union, get_args
from pydantic import BaseModel, Field, create_model

from jadnvalidation.models.pyd.primitives import String, Integer
from jadnvalidation.models.pyd.structures import Record, Array
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

def update_static_types():
    
    String_cls = str_to_class('String')
    Integer_cls = str_to_class('Integer')
    
    Record_cls = str_to_class('Record')
    Array_cls = str_to_class('Array')
    
    model_1 = create_model(
        "model_1",
        name=(String_cls, Field(description='custom string description', min_length=6, max_length=50)), 
        age=(Integer_cls, Field(description='custom integer description', ge=1, le=10))
    )   
    
    model_2 = create_model(
        "model_2",
        record=(Record_cls, Field(description='custom record description', min_length=3, max_length=3)),
        array=(Array_cls, Field(description='custom list description', min_length=2, max_length=4))
    ) 
    
    return_dict = {}
    return_dict["model_1"] = model_1    
    return_dict["model_2"] = model_2
    
    return return_dict


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
    
# class TestBaseModel(BaseModel):
#     @classmethod
#     def with_fields(cls, **field_definitions):
#         return create_model('ModelWithFields', __base__=cls, **field_definitions)    
    
# class TestSchema(BaseModel):
#     types: dict[str, Union[String, Integer]] = Field(default_factory=dict)
    
#     def model_post_init(self, __context):
#         # self.foo = [s.replace("-", "_") for s in self.foo]
#         # updated_types = update_static_types()
#         # self.types = update_types 
#         # my_new_dict={"key3": 3, "key4": 4}
        
#         MyModel = create_model(
#             "MyModel",
#             name=(String, Field(description='custom string description', min_length=6, max_length=50)), 
#             age=(Integer, Field(description='custom integer description', ge=1, le=10))
#         )       
        
#         my_new_dict = {}
#         my_new_dict["test1"] = MyModel      
#         self.types.update(my_new_dict)
#         test = "" 
    
    # def __init__(self, **kwargs):
    #     if "types" in kwargs:
    #         updated_types = update_static_types()
    #         kwargs["types"] = updated_types
    #         super().__init__(**kwargs)
    #         test = ""        
            
            # super().__init__(**kwargs)
            # self.__pydantic_fields__.types = updated_types
            # test = "hit"            
            # kwargs["types"] = update_static_types()
        # super().__init__(**kwargs)
        # self.types = udpated_types
        
class Pet(BaseModel):
    """All my pets"""
    # _types: Dict[str, type] = {}
    _types: ClassVar[Dict[str, type]] = {}
    
    name: str = None
    
    # used to auto-register submodels in _types
    # def __init_subclass__(cls, **kwargs):
    #     return super().__init_subclass__(**kwargs)
    def __init_subclass__(cls, type: Optional[str] = None):
        cls._types[type or cls.__name__.lower()] = cls
        
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, value: Dict[str, Any]) -> 'Pet':
        try:
            pet_type = value.pop('type')
            # init with right Prt submodel
            return cls._types[pet_type](**value)
        except:
            raise ValueError('...')
        
# Cat class will be registered as 'cat'
class Cat(Pet):
    age: int = 2
    
# Dog class will be registered as 'doggy'
# class Dog(Pet, type='dog'):
class Dog(Pet):
    name: str = "Ace"
    food: str = "Blue Buffalo Wilderness"
    
class Person(BaseModel):
    pets: List[Pet] = []    