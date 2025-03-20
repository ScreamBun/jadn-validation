
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_enum():
    root = "Root-Test"    
  
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", [], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_data_list = ['clubs','spades']
    invalid_data_list = [{'SuitEnum': 'asdfghjklasdfghjkl'}, {'SuitEnum': 'Aces'}, {'SuitEnum': 10},'asdfghjklasdfghjkl', 'Aces', 10]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_enum_ids():
    root = "Root-Test"    
  
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["="], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_data_list = [10, 40]
    invalid_data_list = ['asdfghjklasdfghjkl', 'Aces', '10']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    