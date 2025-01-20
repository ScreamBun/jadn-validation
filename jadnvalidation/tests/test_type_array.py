from __future__ import annotations
from typing import List
from pydantic import Field, ValidationError, create_model
from jadnvalidation.models.pyd.schema import Schema
from jadnvalidation.models.pyd.structures import Record
from jadnvalidation.pydantic_schema import create_pyd_model, data_validation

def test_forward_ref():
    
    j_schema =   {  
        "types": [
            ["RecordName1", "Record", [], "", [
                [1, "field_value_1a", "RecordName2", [], ""]
            ]],
            ["RecordName2", "Record", [], "", [
                [1, "field_value_2a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_1 = {
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2a': 'Anytown'
        }             
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

def test_arrays():
    
    j_schema = {
        "types": [
            ["Array-Name-1", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Array-Name-2", [], ""]
            ]],
            ["Array-Name-2", "Array", [], "", [
                [1, "field_value_a", "String", [], ""],
                [2, "field_value_b", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_1 = {
        'Array-Name-1': {
            'field_value_1': "test field",
            'field_value_2': True,
            'field_value_3': ['a value', 'a different value, or not']
        },
        'Array-Name-2': {
            'field_value_a': "test field",
            'field_value_b': 'Anytown'
        }        
    }
    
    invalid_data_1 = {
        'Array-Name-1': {
            'field_value_1a': True,
            'field_value_2a': 'Anytown'
        },
        'Array-Name-2': {
            'field_value_1b': "test field",
            'field_value_2b': False
        }        
    }
    
    err_count = 0
    custom_schema = {}
    try :
        custom_schema = create_pyd_model(j_schema)
    except Exception as err:
        err_count = err_count + 1
        print(err)    
    
    try :
        custom_schema.model_validate(valid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)     
        
    try :
        custom_schema.model_validate(invalid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)        
               
    assert err_count == 1
    
        