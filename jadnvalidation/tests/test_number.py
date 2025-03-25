from jadnvalidation.tests.test_utils import validate_valid_data


def test_type_num():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", [], "", []]
      ]
    }
      
    valid_data_list = [1.5]      
    invalid_data_list = ["1.7z5", "0.0.0.0.0.0.0.0.1.2", "555,", "  555  "]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)