from pydantic import ValidationError
from jadnvalidation.data_validation.data_validation import DataValidation


def test_boolean():
    root = "Boolean-Test"
    
    j_schema = {
      "types": [
        ["Boolean-Test", "Boolean", [], ""]
      ]
    }
    
    valid_data_list = [
        True
    ]
    
    invalid_data_list = [
        {'Boolean-Test': 'True'},
        {'Boolean-Test': 'zzz'},
        {'Boolean-Test': '__false__'}
    ]
    
    err_count = 0
    for data in valid_data_list:
        try:
            j_validation = DataValidation(j_schema, root, data)
            j_validation.validate()
        except ValidationError as e:
            error_count = error_count + 1
            print(e)
        
    assert err_count == 0 
            
    for data in invalid_data_list:
        try :
            j_validation = DataValidation(j_schema, root, data)
            j_validation.validate()
        except Exception as err:
            print(err)
            err_count += 1      
        
    assert err_count == 3