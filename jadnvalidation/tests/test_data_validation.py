from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.tests.test_utils import validate_valid_data


def test_data_validation():  
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", ["{3", "}3"], "", [
                [1, "field_value_1", "String", ["{2"], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            { "Root-Test": ["test", True, 123] },
        ]  
    
    invalid_data_list = [
            { "Root-Test": ["test", True] },
            { "Root-Test": "test" },
            { "Root-Test": ["t", "test", "test", 123, "test", "test", False] }
        ]        
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)