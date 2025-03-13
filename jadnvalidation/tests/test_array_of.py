from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data

def test_array_of_records():
    root = "Root-Test"
    
    # j_schema =   {  
    #     "types": [
    #         ["Root-Test", "Array", [], "", [
    #             [1, "field_value_1a", "ArrayName2", [], ""]
    #         ]],
    #         ["ArrayName2", "Array", [], "", [
    #             [1, "field_value_2a", "String", [], ""]
    #         ]]
    #     ]
    # }
    
    # valid_data_list = [
    #         [['Anytown', 'Any String']],
    #         [['123', '']]
    #     ]
    
    # invalid_data_list = [
    #         [[123, 'Any String']],
    #         'test'
    #     ]
    
    # err_count = validate_valid_data(j_schema, root, valid_data_list)    
    # assert err_count == 0
        
    # err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    # assert err_count == 2
    

def test_array_of_ints():
    root = "Root-Test"    
    
    j_schema = {
        "info": {
            "package": "http://www.test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Integer", "{1", "}3"], ""]
        ]
    }
    
    valid_data_list = [
            [1, -1, 11111111],
            [0, 00, 0]
        ]
    
    invalid_data_list = [
            ["1", 1, 11],
            ["test"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == 2
    
def test_array_of_strs():
    root = "Root-Test"    
    
    j_schema = {
        "info": {
            "package": "http://www.test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*String", "{1", "}3"], ""]
        ]
    }
    
    valid_data_list = [
            ["test", "t", "11111111"],
            ["0", "___", "##"]
        ]
    
    invalid_data_list = [
            ["1", 1, 11],
            ["1", True, False],
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == 2
    
def test_array_of_booleans():
    root = "Root-Test"    
    
    j_schema = {
        "info": {
            "package": "http://www.test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Boolean", "{1", "}3"], ""]
        ]
    }
    
    valid_data_list = [
            [True, False],
            [False, False, True]
        ]
    
    invalid_data_list = [
            ["True", "False", 1],
            ["true", True, False],
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == 2      