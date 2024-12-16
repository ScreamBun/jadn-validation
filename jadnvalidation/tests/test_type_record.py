from typing import Any, Dict, Union
from pydantic import BaseModel, ConfigDict, Field, RootModel, ValidationError, create_model, model_validator
from jadnvalidation.models.pyd.primitives.string import CustomStr, String
from jadnvalidation.models.pyd.schema import Schema
     
     
class TitleCaseStr(str):
    model_config = ConfigDict(arbitrary_types_allowed = True)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        pass       
    
    def __new__(cls, value: str):
        return super().__new__(cls, value.title())     
     
def create_dynamic_model_b(name: str, fields: Dict[str, Any]) -> BaseModel:
    return create_model(name, **fields)


def create_dynamic_model(model_name, fields):
    """Creates a dynamic Pydantic model with custom string fields"""
    model_fields = {}
    for field_name, field_type in fields.items():
        if field_type == "str":
            model_fields[field_name] = (TitleCaseStr, ...)
        else:
            model_fields[field_name] = (field_type, ...)

    return create_model(model_name, **model_fields)


def test_simple_zzz():
    
    # Example usage
    fields = {
        "name": (String, Field(..., description="Name of the object")),
        "age": (int, Field(..., description="Age of the object"))
        # "properties": (Dict[str, Any], Field(..., description="Dynamic properties"))
    }

    model_name = "RootSchema"
    DynamicModel = create_dynamic_model(model_name, fields)
    
    data_b = {
        "name": "MyObject", 
        "age": 10, 
        "properties":{
            "color": "red", "size": "large"
            }
        } 
    
    data = {
        "name": "MyObject", 
        "age": 10
        }           
    
    try:
        DynamicModel.model_validate(data)
        print(DynamicModel)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)    
            
def test_record():
    
    j_schema = {
        "types": [
            ["Record-Name", "Record", ["{1", "}2"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }   
    
    data_1 = {
        'Record-Name': {
            'field_value_1': "test field",
            'field_value_2': 'Anytown'
        }
    }
    
    data_2 = {
            'field_value_1': "test field",
            'field_value_2': 'Anytown'
    }    
    
    data_invalid_1 = {
        'Record-Name': {
            'field_value_1': 123,
            'field_value_2': 'Anytown'
        }
    }    
    
    data_invalid_2 = {
        'field_value_1': 123,
        'field_value_2': 'Anytown'
    }     
    
    custom_model = None    
    error_count = 0
    
    try:
        # custom_model = Schema.model_validate(j_schema)
        custom_model = Schema(**j_schema)
        custom_model.model_rebuild()
        print(custom_model)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
    
    try:
        custom_model.model_validate(data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_model.model_validate(data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
    
    try:
        custom_model.model_validate(data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_model.model_validate(data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    assert error_count == 1
