import sys
from typing import Any, Dict
from pydantic import BaseModel, Field, ValidationError, ValidationInfo, create_model, model_validator
from jadnvalidation.models.pyd.schema import Person, Pet, Schema
from jadnvalidation.models.pyd.structures import Array, Record, RecordOld
from jadnvalidation.models.pyd.primitives import Integer
     

def create_dynamic_model(name: str, fields: dict) -> BaseModel:
    return create_model(name, **fields)

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


# def test_adding_fields_to_existing_model():
#     my_dict={"key1": 1, "key2": 2}
    
#     NewModel = TestBaseModel.with_fields(baz=(int, ...))
    
    
#     valid_data = { 
#         "test1" : {
#             "name" : "Napoleon",
#             "age" : 55    
#         }
#     }    
    
#     try :
#         NewModel(foo='awe')
#     except Exception as err:
#         print(err)  
        
        
def test_list_of_models():
    
    Address = create_model(
        "Address",
        house_number=(str, ...),
        street_name=(str, ...),
        city=(str, ...),
        zip_code=(str, ...),
        model_opts=(str, Field(default="testing model opts", exclude=True, evaluate=False)),
        global_opts=(str, Field(default="testing global opts", exclude=True, evaluate=False)),
        __base__=RecordOld
    )
    
    Person = create_model(
        "Person",
        name=(str, ...),  # Required field
        age=(int, ...),
        address=(Address, ...),  # Nested model field
        model_opts=(str, Field(default="testing model opts", exclude=True, evaluate=False)),
        global_opts=(str, Field(default="testing global opts", exclude=True, evaluate=False)),
        __base__=RecordOld
    ) 
    
    valid_data = {
        "name" : "roberts",
        "age" : 100,
        "address" : {
            "house_number" : "8888",
            "street_name" : "bats lane",
            "city" : "gotham",
            "zip_code" : "22222",
        }
    }
    
    invalid_data = {
        "name" : "roberts",
        "age" : 100,
        "address" : {
            "house_number" : True,
            "street_name" : "bats lane",
            "city" : "gotham",
            "zip_code" : "22222",
        }
    }     
    
    err_count = 0
    try :
        Person.model_validate(valid_data)    
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        Person.model_validate(invalid_data)    
    except Exception as err:
        err_count = err_count + 1
        print(err)        
               
    assert err_count == 1

# def test_dict_of_models():
    
#     j_schema = {
#         "types": [
#             ["Record-Name", "Record", ["{1", "}2"], "", [
#                 [1, "field_value_1", "String", [], ""],
#                 [2, "field_value_2", "String", [], ""]
#             ]]
#         ]
#     } 
    
#     try:
#         # custom_model = Schema.model_validate(j_schema)
#         # custom_model = TestSchema(**j_schema) 
#         # custom_model.model_rebuild()
        
#         # ta = TypeAdapter(List[Any])
#         # m = ta.validate_python(users)    
        
#         # print(custom_model)
#     except ValidationError as e:
#         error_count = error_count + 1
#         print(e)    
    

def test_model_validate():
    
    String_cls = str_to_class('String')
    Integer_cls = str_to_class('Integer')
    
    Record_cls = str_to_class('Record')
    Array_cls = str_to_class('Array')
    
    MyModel = create_model(
        "MyModel",
        name=(String_cls, Field(description='custom string description', min_length=6, max_length=50)), 
        age=(Integer_cls, Field(description='custom integer description', ge=1, le=10)),
        record=(Record_cls, Field(description='custom record description', min_length=3, max_length=3)),
        array=(Array_cls, Field(description='custom list description', min_length=2, max_length=4))
    )  
    
    valid_data = {
        "name" : "Napoleon",
        "age" : 5,
        "record" : { 
            "key1" : "val1",
            "key2" : "val2",
            "key3" : "val3"
            },
        "array" : ["item 1", "item 2"]
    }
    
    invalid_data = {
        "name" : "Pedro",
        "age" : 99,
        "record" : { 
            "key1" : "val1"
            },
        "array" : ["item 1"]
    }    
    
    err_count = 0
    try :
        MyModel.model_validate(valid_data)    
    except Exception as err:
        print(err)   
        
    try :
        MyModel.model_validate(invalid_data)    
    except Exception as err:
        err_count = err_count + 1
        print(err)           
        
    assert err_count == 1

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
