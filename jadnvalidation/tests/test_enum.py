from jadnvalidation.tests.test_utils import create_testing_model, validate_valid_data

def test_enum():
  
    j_schema = {
        "types": [
            ["SuitEnum", "Enumerated", [], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_data_list = [{'SuitEnum': 'clubs'}, {'SuitEnum': 'spades'}]
    invalid_data_list = [{'SuitEnum': 'asdfghjklasdfghjkl'}, {'SuitEnum': 'Aces'}, {'SuitEnum': 10}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_enum_ids():
  
    j_schema = {
        "types": [
            ["SuitEnum", "Enumerated", ["="], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_data_list = [{'SuitEnum': 10}, {'SuitEnum': 40}]
    invalid_data_list = [{'SuitEnum': 'asdfghjklasdfghjkl'}, {'SuitEnum': 'Aces'}, {'SuitEnum': 'clubs'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)    