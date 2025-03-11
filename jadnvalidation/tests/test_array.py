from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data

def test_forward_ref():
    root = "Root-Test"
    
    j_schema =   {  
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1a", "ArrayName2", [], ""]
            ]],
            ["ArrayName2", "Array", [], "", [
                [1, "field_value_2a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [['Anytown', 'Any String']],
            [['123', '']]
        ]
    
    invalid_data_list = [
            [[123, 'Any String']],
            'test'
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == 2
    

def test_array():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            ["test", True, 123],
            ["", False, 0]
        ]
    
    invalid_data_list = [
            [True, "Test", 123],
            ["test"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == 2