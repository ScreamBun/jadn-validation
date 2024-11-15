from pydantic import ValidationError
from jadnvalidation.pydantic_schema import create_pyd_model


def test_boolean():
  
    jadn_schema = {
      "types": [
        ["Boolean-Test", "Boolean", [], ""]
      ]
    }
    
    valid_data_1 = {'Boolean-Test': True}
    valid_data_2 = {'Boolean-Test': 'True'}
    invalid_data_1 = {'Boolean-Test': 'zzz'}
    invalid_data_2 = {'Boolean-Test': '__false__'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                     
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)            
        
    assert error_count == 2