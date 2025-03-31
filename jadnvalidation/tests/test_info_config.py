from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_max_string():
    root = "Root-Test" 
      
    j_schema = {
        "info": {
        "package": "http://test/v1.0",
        "title": "Test Title",
        "exports": ["Root-Test"],
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
            ["Root-Test", "String", [], ""]
        ]
    }
    
    valid_data_list = ['asdfghjk']
    invalid_data_list = ['asdfghjklasdfghjkl']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_max_string_order_of_precedence():
    root = "Root-Test"    
  
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Root-Test"],
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
            ["Root-Test", "String", ["}5"], ""]
        ]
    }
    
    valid_data_list = ['asdfg']
    invalid_data_list = ['asdfghjklasdfghjkl']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_max_binary():
    root = "Root-Test"    
  
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "config": {
            "$MaxBinary": 5,
            "$MaxString": 255,
            "$MaxElements": 100,
            "$Sys": "$",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
            },
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Binary", [], ""]
        ]
    }
    
    valid_data_list = [b"test"]
    invalid_data_list = [b"testing"]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_max_binary_order_of_precedence():
    root = "Root-Test"     
  
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "config": {
            "$MaxBinary": 10,
            "$MaxString": 255,
            "$MaxElements": 100,
            "$Sys": "$",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
            },
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Binary", ["}2"], ""]
        ]
    }
    
    valid_data_list = [ b"zz"]
    invalid_data_list = [b"testing"]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_max_elements_record():
    root = "Root-Test"
  
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Root-Test"],
            "config": {
            "$MaxBinary": 255,
            "$MaxString": 255,
            "$MaxElements": 2,
            "$Sys": "$",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
            }
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["{0"], ""]
            ]]
        ]
    }
    
    valid_data_list =   [
                            {
                                "field_value_1" : "test",
                                "field_value_2" : "test"
                            }
                        ]
    
    invalid_data_list = [
                            {
                                "field_value_1" : "test",
                                "field_value_2" : "test",
                                "field_value_3" : "test"
                            }
                        ]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_sys_indicator():
    root = "Root-Test"
    
    invalid_j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Root-Test"],
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
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "$field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }    
    
    valid_j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Root-Test"],
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
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list =   [
                            {
                                "field_value_1" : "test",
                                "field_value_2" : "test"
                            }
                        ]    
  
    err_count = validate_valid_data(valid_j_schema, root, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(invalid_j_schema, root, valid_data_list)    
    assert err_count == 1
    
def test_type_name_regex():
    invalid_root = "root-test"
    root = "Root-Test"
  
    invalid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["root-test"],
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
            ["record-test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Root-Test"],
            "config": {
            "$MaxBinary": 255,
            "$MaxString": 255,
            "$MaxElements": 100,
            "$Sys": "&",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
            }
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list =   [
                            {
                                "field_value_1" : "test",
                                "field_value_2" : "test",
                                "field_value_3" : "test"
                            }
                        ]    
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(invalid_j_schema_1, invalid_root, valid_data_list)    
    assert err_count == 1
    
def test_field_name_regex():
    root = "Root-Test"    
  
    invalid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Root-Test"],
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
            ["Root-Test", "Record", [], "", [
                [1, "FIELD_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Root-Test"],
            "config": {
            "$MaxBinary": 255,
            "$MaxString": 255,
            "$MaxElements": 100,
            "$Sys": "&",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
            }
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list =   [
                            {
                                "field_value_1" : "test",
                                "field_value_2" : "test",
                                "field_value_3" : "test"
                            }
                        ]    
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(invalid_j_schema_1, root, valid_data_list)    
    assert err_count == 1   
