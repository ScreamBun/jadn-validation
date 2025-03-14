
from jadnvalidation.tests.test_utils import validate_valid_data


def test_map():
    # TODO: Leftoff here.....
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Map-Name"]
        },
        "types": [
            ["String-Name", "String", ["{0"], ""],
            ["Map-Name", "Map", [], "", [
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
                "exports": ["Map-Name"]
            },
            "types": [
                ["Map-Name", "Map", ["{1", "}3"], "", [
                    [1, "field_value_1", "String", [], ""],
                    [2, "field_value_2", "String", [], ""]
                ]]
            ]
        }
    
    valid_data_list = [
            {
                "Map-Name": {
                    "field_value_1": "placeat repellendus sit",
                    "field_value_2": "molestias, sit elit. sit"
                }
            }, 
            {
                "Map-Name": {
                    "field_value_1": "molestias, amet nobis",
                    "field_value_2": "repellendus architecto"
                }
            }
    ]
    
    invalid_data_list = [
        {
            "Map-Name": {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit",
                "field_value_3": "test extra field validation"
            }
        }, 
        {
            "Map-Name": {
                "field_value_x": "test incorrect field name"
            }
        },
        {
            "Map-Name": {
                "field_value_1": 123
            }
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_map_id():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Map-Name"]
        },
        "types": [
            ["Map-Name", "Map", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "Map-Name": {
                    "1": "placeat repellendus sit",
                    "2": "molestias, sit elit. sit"
                }
            }, 
            {
                "Map-Name": {
                    "1": "molestias, amet nobis",
                    "2": "repellendus architecto"
                }
            }
    ]
    
    invalid_data_list = [
        {
            "Map-Name": {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            }
        }, 
        {
            "Map-Name": {
                    "1": True,
                    "2": "repellendus architecto"
            }
        },
        {
            "Map-Name": {
                    "1": "molestias, amet nobis"
            }
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_map_ref_field():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Map-Name"]
        },
        "types": [
            ["IntegerTest", "Integer", ["{0"], ""],
            ["StringTest", "String", ["{0"], ""],
            ["Map-Name", "Map", [], "", [
                [1, "field_value_1", "IntegerTest", [], ""],
                [2, "field_value_2", "StringTest", [], ""]
            ]],
            ["RecordTest", "Record", ["{0"], "", [
                [1, "field_value_1", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "Map-Name": {
                    "field_value_1": 123,
                    "field_value_2": "molestias, sit elit. sit"
                }
            }, 
            {
                "Map-Name": {
                    "field_value_1": 321,
                    "field_value_2": "repellendus architecto"
                }
            }
    ]
    
    invalid_data_list = [
        {
            "Map-Name": {
                "field_value_1": 123,
                "field_value_2": "molestias, sit elit. sit",
                "field_value_3": "test extra field validation"
            }
        }, 
        {
            "Map-Name": {
                "field_value_x": "test incorrect field name"
            }
        },
        {
            "Map-Name": {
                "field_value_1": True
            }
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)     