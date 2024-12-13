from pydantic import ValidationError
from jadnvalidation.models.pyd.schema import Schema
     
            
def test_record():
    
    j_schema = {
        "types": [
            ["Record-Name", "Record", ["{1", "}2"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }   
    
    data_1x = {
        'Record-Name': {
            'field_value_1': "test field",
            'field_value_2': 'Anytown'
        }
    }
    
    data_1 = {
            'field_value_1': "test field",
            'field_value_2': 'Anytown'
    }    
    
    data_invalid_1 = {
        'Record-Name': {
            'field_value_1': 123,
            'field_value_2': 'Anytown'
        }
    }    
    
    custom_model = None    
    error_count = 0
    
    try:
        custom_model = Schema.model_validate(j_schema)
        # custom_model.model_rebuild()
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
        custom_model.model_validate(data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)          
        
    assert error_count == 1
