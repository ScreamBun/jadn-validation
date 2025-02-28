from __future__ import annotations
import time
from pydantic import Field, create_model
from jadnvalidation.models.pyd.structures import Record
from jadnvalidation.pydantic_schema import create_pyd_model, pyd_data_validation
from jadnvalidation.tests.test_utils import create_testing_model, validate_invalid_data, validate_valid_data


def test_nested_static_models():

    Person = create_model(
        "Person",
        name=(str, ...),  # Required field
        age=(int, ...),
        address=('Address', ...),  # Nested model field
        model_opts=(str, Field(default="testing model opts", exclude=True, evaluate=False)),
        global_opts=(str, Field(default="testing global opts", exclude=True, evaluate=False)),
        __base__=Record
    ) 
    
    Address = create_model(
        "Address",
        house_number=(str, ...),
        street_name=(str, ...),
        city=(str, ...),
        zip_code=(str, ...),
        model_opts=(str, Field(default="testing model opts", exclude=True, evaluate=False)),
        global_opts=(str, Field(default="testing global opts", exclude=True, evaluate=False)),
        __base__=Record
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
    
    valid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2a': 'Anytown'
        }             
    }]
    
    invalid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2zzzz': False
        }
    },
    { 'true' : 'True' },
    {}]                         
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_forward_ref_deeper():
    
    j_schema =   {  
        "types": [
            ["RecordName1", "Record", [], "", [
                [1, "field_value_1a", "RecordName2", [], ""]
            ]],
            ["RecordName2", "Record", [], "", [
                [1, "field_value_2a", "RecordName3", [], ""]
            ]],
            ["RecordName3", "Record", [], "", [
                [1, "field_value_3a", "RecordName4", [], ""]
            ]],
            ["RecordName4", "Record", [], "", [
                [1, "field_value_4a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': {
                    'field_value_3a': {
                        'field_value_4a': 'Anytown'
                    }
                }
            }  
        },
        'RecordName2': {
            'field_value_2a': {
                'field_value_3a': {
                    'field_value_4a': 'Anytown'
                }
            }
        },
        'RecordName3': {
            'field_value_3a': {
                'field_value_4a': 'Anytown'
            }
        },
        'RecordName4': {
            'field_value_4a': 'Anytown'
        }               
    }]
    
    invalid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2zzzz': False
        }             
    },
    { 'true' : 'True' },
    {}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
          
    err_count = validate_invalid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)  

def test_records_min_max():
    
    j_schema = {
        "types": [
            ["Record-Name1", "Record", ["{2", "}2"], "", [
                [1, "field_value_1a", "String", ["{0", "[0"], ""],
                [2, "field_value_2a", "String", ["{0", "[0"], ""],
                [3, "field_value_3a", "String", ["{0", "[0"], ""]
            ]],
            ["Record-Name2", "Record", ["{2", "}2"], "", [
                [1, "field_value_1b", "String", ["{0", "[0"], ""],
                [2, "field_value_2b", "String", ["{0", "[0"], ""],
                [3, "field_value_3b", "String", ["{0", "[0"], ""]            
            ]]
        ]
    }  
    
    valid_data_list = [{
        'Record-Name1': {
            'field_value_1a': "test field",
            'field_value_2a': 'Anytown'
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': 'Anytown'
        }        
    }]
    
    invalid_data_list = [{
        'Record-Name1': {
            'field_value_1a': "test field"
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': "test field",
            'field_value_3b': "test field"
        }        
    }]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_records():
    
    j_schema = {
        "types": [
            ["Record-Name1", "Record", ["{1", "}2"], "", [
                [1, "field_value_1a", "String", [], ""],
                [2, "field_value_2a", "String", [], ""]
            ]],
            ["Record-Name2", "Record", ["{1", "}2"], "", [
                [1, "field_value_1b", "String", [], ""],
                [2, "field_value_2b", "String", [], ""]
            ]]            
        ]
    }  
    
    valid_data_list = [{
        'Record-Name1': {
            'field_value_1a': "test field",
            'field_value_2a': 'Anytown'
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': 'Anytown'
        }        
    }]
    
    invalid_data_list = [{
        'Record-Name1': {
            'field_value_1a': True,
            'field_value_2a': 'Anytown'
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': False
        }        
    }]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list) 
