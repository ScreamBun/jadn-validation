from pydantic import ValidationError
from jadnvalidation.pydantic_schema import create_pyd_model


def test_array_min_max_items():
    jadn_schema = {
        "types": [
            ["Array-Name", "Array", ["{1", "}2"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Integer", [], ""]
            ]]
        ]        
    }
    
    valid_data_1 = { 'Array-Name' : [1, "February"] }
    invalid_data_1 = { 'Array-Name' : [1, "February", "March", "April", "May", "June", "July"] }    
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0
    
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1
    

def test_array_str_and_int():
    jadn_schema = {
        "types": [
            ["Array-Name", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Integer", [], ""]
            ]]
        ]        
    }
    
    valid_data_1 = { 'Array-Name' : [1, "February", "March", "April", "May", "June", "July"] }
    invalid_data_1 = { 'Array-Name' : [False, "February", "March", "April", "May", "June", "July"] }    
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0
    
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1        
        

def test_array_str():
    
    jadn_schema = {
        "types": [
            ["Array-Name", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]        
    }
    
    valid_data_1 = { 'Array-Name' : ["January", "February", "March", "April", "May", "June", "July"] }
    invalid_data_1 = { 'Array-Name' : [12, "February", "March", "April", "May", "June", "July"] }
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0
    
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1        