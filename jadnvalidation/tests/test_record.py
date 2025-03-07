from jadnvalidation.tests.test_utils import create_testing_model, validate_invalid_data, validate_valid_data
from jadnvalidation.utils.general_utils import create_data_validation_instance


def test_forward_ref():
    
    j_schema =   {  
        "types": [
            ["RecordName1", "Record", [], "", [
                [1, "field_value_1a", "RecordName2", [], ""]
            ]],
            ["RecordName2", "Record", [], "", [
                [1, "field_value_2a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2a': 'Anytown'
        }             
    }]
    
    invalid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2zzzz': False
        }
    },
    { 'true' : 'True' },
    {}]                         
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_forward_ref_deeper():
    
    j_schema =   {  
        "types": [
            ["RecordName1", "Record", [], "", [
                [1, "field_value_1a", "RecordName2", [], ""]
            ]],
            ["RecordName2", "Record", [], "", [
                [1, "field_value_2a", "RecordName3", [], ""]
            ]],
            ["RecordName3", "Record", [], "", [
                [1, "field_value_3a", "RecordName4", [], ""]
            ]],
            ["RecordName4", "Record", [], "", [
                [1, "field_value_4a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': {
                    'field_value_3a': {
                        'field_value_4a': 'Anytown'
                    }
                }
            }  
        },
        'RecordName2': {
            'field_value_2a': {
                'field_value_3a': {
                    'field_value_4a': 'Anytown'
                }
            }
        },
        'RecordName3': {
            'field_value_3a': {
                'field_value_4a': 'Anytown'
            }
        },
        'RecordName4': {
            'field_value_4a': 'Anytown'
        }               
    }]
    
    invalid_data_list = [{
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2zzzz': False
        }             
    },
    { 'true' : 'True' },
    {}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
          
    err_count = validate_invalid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)  

def test_records_min_max():
    
    j_schema = {
        "types": [
            ["Record-Name1", "Record", ["{2", "}2"], "", [
                [1, "field_value_1a", "String", ["{0", "[0"], ""],
                [2, "field_value_2a", "String", ["{0", "[0"], ""],
                [3, "field_value_3a", "String", ["{0", "[0"], ""]
            ]],
            ["Record-Name2", "Record", ["{2", "}2"], "", [
                [1, "field_value_1b", "String", ["{0", "[0"], ""],
                [2, "field_value_2b", "String", ["{0", "[0"], ""],
                [3, "field_value_3b", "String", ["{0", "[0"], ""]            
            ]]
        ]
    }  
    
    valid_data_list = [{
        'Record-Name1': {
            'field_value_1a': "test field",
            'field_value_2a': 'Anytown'
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': 'Anytown'
        }        
    }]
    
    invalid_data_list = [{
        'Record-Name1': {
            'field_value_1a': "test field"
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': "test field",
            'field_value_3b': "test field"
        }        
    }]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(custom_schema, invalid_data_list)
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
            'field_value_1a': "test field",
            'field_value_2a': 'Anytown'
        },
        {
            'field_value_1b': "test field",
            'field_value_2b': 'Anytown'
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

def test_instance():
    
    root = "Root-Test"
    j_list = []
    data = "test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}2"], "", [
                [1, "field_value_1a", "String", [], ""],
                [2, "field_value_2a", "String", [], ""]
            ]]          
        ]
    }     
    
    # TODO: Leftoff here... need to add this to the flection logic to hopefully remove circular dependencis with imports
    instance = create_data_validation_instance("jadnvalidation.data_validation.string", "String", j_schema, j_list, data)
    instance.validate()