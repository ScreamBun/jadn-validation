from pydantic import ValidationError
from jadnvalidation.models.pyd.schema import Schema
from jadnvalidation.pydantic_schema import create_pyd_model

# def create_dynamic_model(schema: dict):
#     """Creates a Pydantic model dynamically from a nested dictionary schema."""

#     fields = {}

#     for field_name, field_info in schema.items():
#         if isinstance(field_info, dict):
#             # If the field is a nested dictionary, recursively create a nested model
#             fields[field_name] = (create_dynamic_model(field_info), ...)
#         else:
#             # Otherwise, use the field type directly
#             fields[field_name] = (field_info, ...)

#     return create_model('DynamicModel', **fields)

# Left off here, convert to use JADN, model above pattern

            
def test_record():
    
    j_schema = {
        "types": [
            ["Record-Name", "Record", [], "", [
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
    
    data_invalid_1 = {
        'Record-Name': {
            'field_value_1': 123,
            'field_value_2': 'Anytown'
        }
    }    
    
    custom_model = create_pyd_model(j_schema)    
    print(custom_model)
    error_count = 0
    
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
    
def test_record_min_max():
    
    j_schema = { 
        "types": [
            ["Record-Name", "Record", ["X", "{1", "}1", "otrue"], "", [
                [1, "field_value_1", "String", [], ""],
                [1, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    data_1 = {
        'Record-Name': {
            'field_value_1': "test field",
            'field_value_2': "test field"
        }
    }
    
    data_invalid_1 = {
        'Record-Name': {
            'field_value_1': 123,
            'field_value_2': 'Anytown'
        }
    }    
    
    custom_model = create_pyd_model(j_schema)    
    print(custom_model)
    error_count = 0
    
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
    
def test_init():
    
    error_count = 0
    
    j_schema = { 
        "types": [
            ["Record-Name", "Record", ["X", "{1", "}1", "otrue"], "", [
                [1, "field_value_1", "String", [], ""],
                [1, "field_value_2", "String", [], ""]
            ]]
        ]
    }    
    
    Schema.model_validate(j_schema)
    
    assert error_count == 0