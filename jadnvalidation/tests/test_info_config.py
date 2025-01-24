from pydantic import ValidationError
from jadnvalidation.pydantic_schema import create_pyd_model, data_validation


def test_max_string():
  
    jadn_schema = {
        "info": {
        "package": "http://test/v1.0",
        "title": "Test Title",
        "exports": ["String-Name"],
        "config": {
            "$MaxBinary": 255,
            "$MaxString": 10,
            "$MaxElements": 100,
            "$Sys": "$",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
        }
        },
        "types": [
            ["String-Name", "String", [], ""]
        ]
    }
    
    valid_data_1 = {'String-Name': 'asdfghjk'}
    invalid_data_1 = {'String-Name': 'asdfghjklasdfghjkl'}
    
    error_count = 0
    pyd_model = {}
    
    try :
        pyd_model = create_pyd_model(jadn_schema)
    except Exception as err:
        err_count = err_count + 1
        print(err)        
        
    try :
        data_validation(pyd_model, valid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)           
        
    assert error_count == 0        
        
    try:
        data_validation(pyd_model, invalid_data_1)
    except Exception as e:
        error_count = error_count + 1
        print(e)         
        
    assert error_count == 1
    
def test_max_string_order_of_precedence():
  
    jadn_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["String-Name"],
            "config": {
            "$MaxBinary": 255,
            "$MaxString": 255,
            "$MaxElements": 100,
            "$Sys": "$",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
            }
        },
        "types": [
            ["String-Name", "String", ["}5"], ""]
        ]
    }
    
    valid_data_1 = {'String-Name': 'asdf'}
    invalid_data_1 = {'String-Name': 'asdfghjklasdfghjkl'}
    
    error_count = 0
    pyd_model = {}
    
    try :
        pyd_model = create_pyd_model(jadn_schema)
    except Exception as err:
        err_count = err_count + 1
        print(err)        
        
    try :
        data_validation(pyd_model, valid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)           
        
    assert error_count == 0        
        
    try:
        data_validation(pyd_model, invalid_data_1)
    except Exception as e:
        error_count = error_count + 1
        print(e)         
        
    assert error_count == 1    