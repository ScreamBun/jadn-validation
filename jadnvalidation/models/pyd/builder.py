from collections import namedtuple
from typing import Callable, Dict, Optional, Type, Union

from pydantic import create_model

from jadnvalidation.consts import FieldAlias
from jadnvalidation.models.jadn.options import Options
from jadnvalidation.models.jadn.primitives import Binary, Boolean, Integer, Number, String

Primitive = Union[Binary, Boolean, Integer, Number, String]
Structure = Union[Array, ArrayOf, Choice, Enumerated, Map, MapOf, Record]
Definition = Union[Primitive, Structure]
jadn_def = namedtuple("jadn_def", ("name", "type", "options", "description", "fields"), defaults=(None, None, [], "", []))

# Leftoff here... filling things in... 

def make_def(data: list, formats: Dict[str, Callable] = None) -> Type[Definition]:
    """
    Create a custom definition with the given arguments
    :param data: the original JADN for the definition
    :param formats: the JADN format validators
    :return: type definition class
    """
    def_obj = jadn_def(*data)
    if cls := DefTypes.get(def_obj.type):
        cls_kwargs = {}
        fields = {}
        if def_obj.type == "Enumerated":
            values = {}
            for field in def_obj.fields:
                field_obj = dict(enum_field(*field)._asdict())
                field_obj["default"] = field_obj["name"]
                values[field_obj.pop("name")] = Field(**field_obj)
            cls_kwargs["__enums__"] = Enum("__enums__", values)
        else:
            for field in def_obj.fields:
                field_obj = dict(def_field(*field)._asdict())
                name = field_obj.pop("name")
                field_obj["options"] = Options(field_obj["options"], name=f"{def_obj.name}.{name}", data_type=field_obj.get("type", "String"), validation=formats)
                if alias := FieldAlias.get(name):
                    field_obj["alias"] = name
                    name = alias

                field_type = clsName(field_obj.get("type", "String"))
                if def_obj.type == "Choice" or field_obj["options"].isOptional():
                    annotation = Optional[field_type]
                    field_obj["required"] = False
                else:
                    annotation = field_type
                    field_obj["required"] = True
                field_info = Field(**field_obj)
                fields[name] = (annotation, field_info)

        alias = clsName(def_obj.name)
        cls_kwargs.update(
            __name__=alias,
            __doc__=def_obj.description,
            __options__=Options(def_obj.options, name=def_obj.name, validation=formats)
        )
        def_model = create_model(alias, __base__=cls, __cls_kwargs__=cls_kwargs, **fields)
        return def_model
    raise TypeError(f"Unknown definition of {def_obj.type}")
