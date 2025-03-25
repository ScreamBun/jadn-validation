
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_map():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            }, 
            {
                "field_value_1": "molestias, amet nobis",
                "field_value_2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit",
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_map_min_max():
    root = "Root-Test"
    
    j_schema = {
            "info": {
                "package": "http://test/v1.0",
                "exports": ["Root-Test"]
            },
            "types": [
                ["Root-Test", "Map", ["{2", "}2"], "", [
                    [1, "field_value_1", "String", [], ""],
                    [2, "field_value_2", "String", [], ""]
                ]]
            ]
        }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            }, 
            {
                "field_value_1": "molestias, amet nobis",
                "field_value_2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit",
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_map_id():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "1": "placeat repellendus sit",
                "2": "molestias, sit elit. sit"
            }, 
            {
                "1": "molestias, amet nobis",
                "2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit"
        }, 
        {
            "1": True,
            "2": "repellendus architecto"
        },
        {
            "1": "molestias, amet nobis"
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_map_ref_field():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["IntegerTest", "Integer", ["{0"], ""],
            ["StringTest", "String", ["{0"], ""],
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "IntegerTest", [], ""],
                [2, "field_value_2", "StringTest", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": 123,
                "field_value_2": "molestias, sit elit. sit"
            }, 
            {
                "field_value_1": 321,
                "field_value_2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": 123,
            "field_value_2": "molestias, sit elit. sit",
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_1": "test incorrect field name"
        },
        {
            "field_value_1": True
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_map_ref_record():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "rec_value_1", "Record-Name", [], ""]
            ]],
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "rec_value_1": {
                    "field_value_1": "test"
                }
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": 123,
            "field_value_2": "molestias, sit elit. sit",
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_1": "test incorrect field name"
        },
        {
            "field_value_1": True
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_map_min_occurs():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", ["[1"], ""],
                [2, "field_value_2", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            },
            {
                "field_value_1": "placeat repellendus sit"
            }            
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "molestias, sit elit. sit"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_map_max_occurs():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", ["1]"], ""],
                [2, "field_value_2", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            },
            {
                "field_value_1": "placeat repellendus sit"
            }            
    ]
    
    invalid_data_list = [
        {
            "field_value_21": "data 1",
            "field_value_11": "data 2"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    
    
# TODO: Test min or max greater than one, which means the data value changes to an array.    