from jadnvalidation.tests.test_utils import validate_valid_data


def test_forward_ref():
    root = "Root-Test"
    
    j_schema =   {  
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_a", "RecordName2", [], ""]
            ]],
            ["RecordName2", "Record", [], "", [
                [1, "field_value_aa", "RecordName3", [], ""]
            ]],
            ["RecordName3", "Record", [], "", [
                [1, "field_value_aaa", "RecordName4", [], ""]
            ]],
            ["RecordName4", "Record", [], "", [
                [1, "field_value_aaaa", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            'field_value_a': {
                'field_value_aa': {
                    'field_value_aaa': {
                        'field_value_aaaa': 'Darth Malgus'
                    }
                }
            }  
        }
    ]
    
    invalid_data_list = [
        {
            'field_value_a': {
                'field_value_aa': {
                    'field_value_aaa': {
                        'field_value_aaaa': 0
                    }
                }
            }  
        },
        {
            'field_value_a': {
                'field_value_aaa': "Dartg Nihilus"
            },
        },
        { 'true' : 'True' },
        {}
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_records_min_max():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{2", "}3"], "", [
                [1, "field_value_1", "String", ["{2", "}6"], ""],
                [2, "field_value_2", "String", ["{2", "}6"], ""],
                [3, "field_value_3", "String", ["{0"], ""]
            ]]
        ]
    }  
    
    valid_data_list = [
        {
            'field_value_1': 'test',
            'field_value_2': '654321'
        },
        {
            'field_value_1': '123456',
            'field_value_2': "apple",
            'field_value_3': 'Sigma'
        }        
    ]

    # TODO: Need to test too many fields...    
    invalid_data_list = [{
        'Record-Name1': {
            'field_value_1': "test field"
        },
        'Record-Name2': {
            'field_value_1': "test field",
            'field_value_2': False,
            'field_value_5': "test field"
        }        
    }]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_record():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}2"], "", [
                [1, "field_value_1a", "String", [], ""],
                [2, "field_value_2a", "String", [], ""]
            ]]          
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1a": "test field",
            "field_value_2a": "Anytown"
        },
        {
            "field_value_1a": "testing more",
            "field_value_2a": "z"
        },
        {
            "field_value_1a": "testing more 123",
            "field_value_2a": "321"
        }        
    ]
    
    invalid_data_list = [
        {
            'field_value_1a': True,
            'field_value_2a': 'Anytown'
        },
        {
            'field_value_1b': "test field",
            'field_value_2b': False
        }        
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_record_in_record():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Record-Test"]
        },
        "types": [
            ["Root-Test", "Record", ["{1", "}2"], "", [
                [1, "field_value_1", "Record2-Test", [], ""]
            ]],
            ["Record2-Test", "Record", ["{1", "}2"], "", [
                [1, "field_value_1b", "String", ["{0", "[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": {
                "field_value_1b": "molestias,"
            }
        }       
    ]
    
    invalid_data_list = [
        {
            'field_value_1b': True
        },
        {
            'field_value_1b': 123
        }        
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    