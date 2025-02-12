from __future__ import annotations
from typing import List, Union

from pydantic import create_model
from jadnvalidation.pydantic_schema import create_pyd_model, data_validation
from jadnvalidation.tests.test_utils import create_testing_model, validate_invalid_data, validate_valid_data

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
        data_validation(custom_schema, valid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        data_validation(custom_schema, invalid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        data_validation(custom_schema, invalid_data_2)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        data_validation(custom_schema, invalid_data_3)        
    except Exception as err:
        err_count = err_count + 1
        print(err)                    
        
    assert err_count == 3
    
def create_dynamic_union(*types):
    return Union[types]

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

    custom_union = create_dynamic_union(int, str, bool)
    list_name = "Array-Test"

    fields = {
        list_name: (List[custom_union], ...)  # Field name "items" with type List[str], required
    }
    
    model = create_model("ArrayModel", **fields)
    
    data = {"Array-Test": [123, "banana", True]}
    
    try :
        model.model_validate(valid_data_list)
    except Exception as err:
        print(err)    
    
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
    
    # custom_schema, err_count = create_testing_model(j_schema)
        
    # err_count = validate_valid_data(custom_schema, valid_data_list)    
    # assert err_count == 0
        
    # err_count = validate_invalid_data(custom_schema, invalid_data_list)
    # assert err_count == len(invalid_data_list)   
    
        