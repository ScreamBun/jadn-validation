from jadnvalidation.tests.test_utils import validate_valid_data, validate_invalid_data


def test_boolean():
    root = "Boolean-Test"
    
    j_schema = {
      "types": [
        ["Boolean-Test", "Boolean", [], ""]
      ]
    }
    # remove and move into a record test {'Boolean-Test': True}
    valid_data_list = [True, False]
    
    invalid_data_list = [{'Boolean-Test': True},'True', 'zzz', '__false__']
      
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    