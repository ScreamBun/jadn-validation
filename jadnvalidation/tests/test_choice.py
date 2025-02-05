from jadnvalidation.tests.test_utils import create_testing_model, validate_valid_data


def test_choice():
    
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Choice-Name"]
        },
        "types": [
            ["Choice-Name", "Choice", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "Choice-Name": {
                "field_value_1": "illum repellendus nobis",
                "field_value_2": True
            }
        }, 
            {
            "Choice-Name": {
                "field_value_2": False
            }
        }
    ]
    
    invalid_data_list = [
        {
            "Choice-Name": {
                "field_value_1": "illum repellendus nobis",
                "field_value_2": True,
                "field_value_3": "test extra field validation"
            }
        }, 
        {
            "Choice-Name": {
                "field_value_x": "test incorrect field name"
            }
        },
        {
            "Choice-Name": {
                "field_value_1": 123
            }
        }        
    ]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    

def test_choice_id():
    
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Choice-Name"]
        },
        "types": [
            ["Choice-Name", "Choice", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "Choice-Name": {
                "1": "illum repellendus nobis",
                "2": True
            }
        }, 
            {
            "Choice-Name": {
                "2": False
            }
        }
    ]
    
    invalid_data_list = [
        {
            "Choice-Name": {
                "field_value_1": "illum repellendus nobis",
                "field_value_2": True,
                "field_value_3": "test extra field validation"
            }
        }, 
        {
            "Choice-Name": {
                "field_value_x": "test incorrect field name"
            }
        },
        {
            "Choice-Name": {
                "1": 123
            }
        }        
    ]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)      