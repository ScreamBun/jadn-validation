import sys
from typing import Any, Dict
from pydantic import BaseModel, Field, ValidationError, ValidationInfo, create_model, field_validator, model_validator
from jadnvalidation.models.pyd.primitives import Integer, String, String, TitleCaseStr
from jadnvalidation.models.pyd.schema import Schema
from jadnvalidation.models.pyd.structures import Array, Record
     

def create_dynamic_model(name: str, fields: dict) -> BaseModel:
    return create_model(name, **fields)


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

def test_model_validate():
    
    String_cls = str_to_class('String')
    Integer_cls = str_to_class('Integer')
    
    Record_cls = str_to_class('Record')
    Array_cls = str_to_class('Array')
    
    MyModel = create_model(
        "MyModel",
        email=(String_cls, Field(description='custom string description')), 
        age=(Integer_cls, Field(description='custom integer description', ge=1, le=10)),
        record=(Record_cls, Field(description='custom record description')),
        array=(Array_cls, Field(description='custom list description'))
    )  
    
    valid_data = {
        "email" : "hello@email.com",
        "age" : 99,
        "record" : { "test" : "dict"},
        "array" : ["item 1", "item 2"]
    }
    
    invalid_data = {
        "email" : "hello",
        "age" : False,
        "record" : None,
        "array" : True
    }    
    
    try :
        # validate_selected_fields_from_model(MyModel, data)
        # DynamicModel.model_rebuild()
        MyModel.model_validate(valid_data)    
    except Exception as err:
        print(err)   
        
    try :
        MyModel.model_validate(invalid_data)    
    except Exception as err:
        print(err)           

class MyString(BaseModel):
    
    @model_validator(mode='after')
    @classmethod
    def validate_model(cls, data: Any, info: ValidationInfo) -> Any:
        test = ""     



class MyModel(BaseModel):
    # my_field: str = Field(..., min_length=3)

    # @field_validator('my_field')
    # def validate_my_field(cls, v):
    #     if not v.isalnum():
    #         raise ValueError("my_field must be alphanumeric")
    #     return v
    
    @model_validator(mode='after')
    @classmethod
    def validate_model(cls, data: Any, info: ValidationInfo) -> Any:
        test = ""
        
def validate_selected_fields_from_model(model:BaseModel, data_dict:Dict):
    for k,v in data_dict.items():
        try:
            model.__pydantic_validator__.validate_assignment(model.model_construct(), k, v )
        except ValidationError as e:
            print(e)        
    
def test_dy_class():
    # Create a field dynamically    
    dy_field1 = Field(..., description="Dynamic field")
    
    # Add the field to the class dict
    MyModel.model_fields["dy_field1"] = dy_field1
    
    # dy_field2 = (MyString, ...)
    # dy_field2 = (TitleCaseStr, ...)
    # MyModel.model_fields["dy_field2"] = dy_field2
    
    MyModel.model_rebuild()
    
    data = {
        "dy_field1" : "hello 1",
        "dy_field2" : "hello 2",
    }
    
    try :
        validate_selected_fields_from_model(MyModel, data)
        # MyModel.model_validate(data)    
    except Exception as err:
        print(err)        
    
    
    # Create an instance of the model, aka test it out
    # model = MyModel(dy_field1="hello", dy_field2="world")

    # print("zzzzzzzzzzzzz: " + str(model))    
     
     
     
# def create_dynamic_model_b(name: str, fields: Dict[str, Any]) -> BaseModel:
#     return create_model(name, **fields)


# def create_dynamic_model(model_name, fields):
#     """Creates a dynamic Pydantic model with custom string fields"""
#     model_fields = {}
#     for field_name, field_type in fields.items():
#         if field_type == "str":
#             model_fields[field_name] = (TitleCaseStr, ...)
#         else:
#             model_fields[field_name] = (field_type, ...)

#     return create_model(model_name, **model_fields)


# def test_simple_zzz():
    
#     # Example usage
#     fields = {
#         "name": (String, Field(..., description="Name of the object")),
#         "age": (int, Field(..., description="Age of the object"))
#         # "properties": (Dict[str, Any], Field(..., description="Dynamic properties"))
#     }

#     model_name = "RootSchema"
#     DynamicModel = create_dynamic_model(model_name, fields)
    
#     data_b = {
#         "name": "MyObject", 
#         "age": 10, 
#         "properties":{
#             "color": "red", "size": "large"
#             }
#         } 
    
#     data = {
#         "name": "MyObject", 
#         "age": 10
#         }           
    
#     try:
#         DynamicModel.model_validate(data)
#         print(DynamicModel)
#     except ValidationError as e:
#         error_count = error_count + 1
#         print(e)    
            
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
