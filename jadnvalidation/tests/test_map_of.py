from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_map_of_int_string():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Integer-Name", "Integer", [], ""],
            ["String-Name", "String", [], ""],
            ["Root-Test", "MapOf", ["+Integer", "*String"], ""]
        ]
    }
    
    valid_data_list = [
            {
                "Root-Test": [1, "asdf", 2, "fdsaf"]
            }
    ]
    
    invalid_data_list = [
            {
                "Root-Test": [1, True, 2, False]
            }
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_map_of_string_string():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["String-Name", "String", [], ""],
            ["Root-Test", "MapOf", ["+String", "*String"], ""]
        ]
    }
    
    valid_data_list = [
            {
                "Root-Test": 
                {
                    "key1" : "val1",
                    "key2" : "val2",
                    "key3" : "val3"
                }       
            }
    ]
    
    invalid_data_list = [
            {
                "Root-Test": 
                {
                    1 : "val1",
                    "key2" : 2,
                    "key3" : True
                }
            }
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)     