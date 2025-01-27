from pydantic import ValidationError
from jadnvalidation.pydantic_schema import create_pyd_model, data_validation
from jadnvalidation.tests.test_utils import create_testing_model, validate_data


def test_max_string():
  
    j_schema = {
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
    
    valid_data_list = [{'String-Name': 'asdfghjk'}]
    invalid_data_list = [{'String-Name': 'asdfghjklasdfghjkl'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_max_string_order_of_precedence():
  
    j_schema = {
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
    
    valid_data_list = [{'String-Name': 'asdf'}]
    invalid_data_list = [{'String-Name': 'asdfghjklasdfghjkl'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_max_binary():
  
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
            "exports": ["Binary-Name"]
        },
        "types": [
            ["Binary-Name", "Binary", [], ""]
        ]
    }
    
    valid_data_list = [{"Binary-Name": b"test"}]
    invalid_data_list = [{"Binary-Name": b"testing"}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_max_binary_order_of_precedence():
  
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
            "exports": ["Binary-Name"]
        },
        "types": [
            ["Binary-Name", "Binary", ["}2"], ""]
        ]
    }
    
    valid_data_list = [{"Binary-Name": b"zz"}]
    invalid_data_list = [{"Binary-Name": b"testing"}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_max_elements_record():
  
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [{ 
                        "Record-Name": {
                            "field_value_1" : "test",
                            "field_value_2" : "test"
                        }
                    }]
    
    invalid_data_list = [{
                        "Record-Name": {
                            "field_value_1" : "test",
                            "field_value_2" : "test",
                            "field_value_3" : "test"
                        }
                    }]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_sys_indicator():
  
    invalid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["$Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    invalid_j_schema_2 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "$String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    invalid_j_schema_3 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
            "config": {
            "$MaxBinary": 255,
            "$MaxString": 255,
            "$MaxElements": 100,
            "$Sys": "%",
            "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
            }
        },
        "types": [
            ["%Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [{ 
                        "Record-Name": {
                            "field_value_1" : "test",
                            "field_value_2" : "test"
                        }
                    }]    
  
    total_errs = 0
    custom_schema, err_count = create_testing_model(invalid_j_schema_1)
    total_errs = total_errs + err_count
    custom_schema, err_count = create_testing_model(invalid_j_schema_2)
    total_errs = total_errs + err_count
    custom_schema, err_count = create_testing_model(invalid_j_schema_3)
    total_errs = total_errs + err_count
    custom_schema, err_count = create_testing_model(valid_j_schema_1)
    total_errs = total_errs + err_count
        
    err_count = validate_data(custom_schema, valid_data_list)    
    total_errs = total_errs + err_count
    
    assert total_errs == 3
    
def test_type_name_regex():
  
    invalid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [{ 
                        "Record-Name": {
                            "field_value_1" : "test",
                            "field_value_2" : "test",
                            "field_value_3" : "test"
                        }
                    }]    
  
    total_errs = 0
    custom_schema, err_count = create_testing_model(invalid_j_schema_1)
    total_errs = total_errs + err_count
    custom_schema, err_count = create_testing_model(valid_j_schema_1)
    total_errs = total_errs + err_count
        
    err_count = validate_data(custom_schema, valid_data_list)    
    total_errs = total_errs + err_count
    
    assert total_errs == 1
    
def test_field_name_regex():
  
    invalid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["Record-Name", "Record", [], "", [
                [1, "FIELD_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_j_schema_1 = {
        "info": {
            "package": "http://test/v1.0",
            "title": "Test Title",
            "exports": ["Record-Name"],
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
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""],
                [3, "field_value_3", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [{ 
                        "Record-Name": {
                            "field_value_1" : "test",
                            "field_value_2" : "test",
                            "field_value_3" : "test"
                        }
                    }]    
  
    total_errs = 0
    custom_schema, err_count = create_testing_model(invalid_j_schema_1)
    total_errs = total_errs + err_count
    custom_schema, err_count = create_testing_model(valid_j_schema_1)
    total_errs = total_errs + err_count
        
    err_count = validate_data(custom_schema, valid_data_list)    
    total_errs = total_errs + err_count
    
    assert total_errs == 1
  
# TODO: Waiting for namespace logic    
# def test_nsid_regex():
  
#     invalid_j_schema_1 = {
#         "info": {
#             "package": "http://test/v1.0",
#             "title": "Test Title",
#             "exports": ["Record-Name"],
#             "config": {
#             "$MaxBinary": 255,
#             "$MaxString": 255,
#             "$MaxElements": 100,
#             "$Sys": "$",
#             "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
#             "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
#             "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
#             }
#         },
#         "types": [
#             ["Record-Name", "Record", [], "", [
#                 [1, "FIELD_value_1", "String", [], ""],
#                 [2, "field_value_2", "String", [], ""],
#                 [3, "field_value_3", "String", ["[0"], ""]
#             ]]
#         ]
#     }
    
#     valid_j_schema_1 = {
#         "info": {
#             "package": "http://test/v1.0",
#             "title": "Test Title",
#             "exports": ["Record-Name"],
#             "config": {
#             "$MaxBinary": 255,
#             "$MaxString": 255,
#             "$MaxElements": 100,
#             "$Sys": "&",
#             "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
#             "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
#             "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
#             }
#         },
#         "types": [
#             ["Record-Name", "Record", [], "", [
#                 [1, "field_value_1", "String", [], ""],
#                 [2, "field_value_2", "String", [], ""],
#                 [3, "field_value_3", "String", [], ""]
#             ]]
#         ]
#     }
    
#     valid_data_list = [{ 
#                         "Record-Name": {
#                             "field_value_1" : "test",
#                             "field_value_2" : "test",
#                             "field_value_3" : "test"
#                         }
#                     }]    
  
#     total_errs = 0
#     custom_schema, err_count = create_testing_model(invalid_j_schema_1)
#     total_errs = total_errs + err_count
#     custom_schema, err_count = create_testing_model(valid_j_schema_1)
#     total_errs = total_errs + err_count
        
#     err_count = validate_data(custom_schema, valid_data_list)    
#     total_errs = total_errs + err_count
    
#     assert total_errs == 1     
    