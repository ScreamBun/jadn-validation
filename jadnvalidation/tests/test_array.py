from __future__ import annotations
from typing import List, Union

from pydantic import Field, create_model
from jadnvalidation.models.pyd.primitives import String
from jadnvalidation.pydantic_schema import create_pyd_model, pyd_data_validation
from jadnvalidation.tests.test_utils import create_testing_model, validate_invalid_data, validate_valid_data
from jadnvalidation.utils.general_utils import create_derived_class, create_dynamic_union

def test_forward_ref():
    # i broke this in the move from record; array broke.jpg
    j_schema =   {  
        "types": [
            ["ArrayName1", "Array", [], "", [
                [1, "field_value_1a", "ArrayName2", [], ""]
            ]],
            ["ArrayName2", "Array", [], "", [
                [1, "field_value_2a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_1 = {
        'ArrayName1': {
            'field_value_1a': ['Anytown']    
        },
        'ArrayName2': ['Anytown']                     
    }
    
    invalid_data_1 = {
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2zzzz': False
        }             
    }
    
    invalid_data_2 = True
    
    invalid_data_3 = {}
    
    err_count = 0
    custom_schema = {}
    try :
        custom_schema = create_pyd_model(j_schema)
    except Exception as err:
        err_count = err_count + 1
        print(err)    
    
    try :
        pyd_data_validation(custom_schema, valid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        pyd_data_validation(custom_schema, invalid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        pyd_data_validation(custom_schema, invalid_data_2)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        pyd_data_validation(custom_schema, invalid_data_3)        
    except Exception as err:
        err_count = err_count + 1
        print(err)                    
        
    assert err_count == 3

class TestClass:
    def __init__(self, name):
        self.name = name

    def display_name(self):
        return f"Name: {self.name}"

    
def test_derived_classes():
    
    # Example usage
    NewClass = create_derived_class(TestClass, "NewClass", {"greet": lambda self: f"Hello, {self.name}!"})
    
    # Instantiate and use the new class
    instance = NewClass("Alice")
    print(instance.display_name())
    print(instance.greet())
    
def test_dynamic_union():
    
    fields1 = {
        "field2": (str, ...),
        "field3": (int, ...)
    }    
    
    model1 = create_model("DynamicUnionModel", **fields1)
    
    custom_union = create_dynamic_union(model1, int, str, bool)
    
    fields2 = {
        "field1": (custom_union, ...)
    }
    
    model = create_model("DynamicUnionModel", **fields2)
    
    data = {"field1": 123}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)
        
    data = {"field1": "banana"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": True}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": 123.45}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "123.45"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "banana"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "True"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "false"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "123"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "banana"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "123.45"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "banana"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "123.45"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "banana"}
    
    try :
        model.model_validate(data)
    except Exception as err:
        print(err)    
    
    data = {"field1": "123.45"}
    

def test_array():
    
    j_schema = {
        "types": [
            ["Array-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            { "Array-Test": ["test", True, 123] },
            { "Array-Test": [123, "test", True] },
            { "Array-Test": ["test", "test", "test"] },
            { "Array-Test": ["test", "test", "test", 123, "test", "test", False] }
        ]
    
    # invalid_data_1 = {
    #     'Array-Name-1': {
    #         'field_value_1a': True,
    #         'field_value_2a': 'Anytown'
    #     },
    #     'Array-Name-2': {
    #         'field_value_1b': "test field",
    #         'field_value_2b': False
    #     }        
    # }
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    # err_count = validate_invalid_data(custom_schema, invalid_data_list)
    # assert err_count == len(invalid_data_list)   
    
def test_array_continued():
    
    j_schema = {
        "types": [
            ["Array-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            { "Array-Test": ["test", True, 123] },
            { "Array-Test": [123, "test", True] },
            { "Array-Test": ["test", "test", "test"] },
            { "Array-Test": ["test", "test", "test", 123, "test", "test", False] }
        ]
    
    # For each J field, create a model and add J field options to the model's field as type opts.
    # Create a model for the list and add the J field models to it as fields
    # Add the list model to the root model 

    # custom_union = create_dynamic_union(int, str, bool)
    
    # pyd_field = (str, Field(...))    
    
    # inner_fields = {
    #     "first_name": (str, ...),
    #     "last_name": (str, ...)
    # }
    
    # inner_model = create_model("ArrayFieldsModel", **inner_fields)
    # globals()["ArrayFieldsModel"] = inner_model
    
    custom_string = String()
    custom_string.__test = "zzzz"
    
    custom_union = create_dynamic_union(custom_string)
    
    fields = {
        "Array-Test": (List[custom_union], ...)
    }
    
    # model = create_model("ArrayModel", **fields)
    
    # data = {"Array-Test": [
    #         # {"ArrayFieldsModel" : 
    #             {
    #                 "first_name" : "sith",
    #                 "last_name" : "bane",
    #             }
    #         # }
    #     ]}
    
    # try :
    #     model.model_validate(data)
    # except Exception as err:
    #     print(err)    
    
    # try :
    #     model.model_validate(valid_data_list)
    # except Exception as err:
    #     print(err)       
        