from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


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
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_num_min_inclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["w2"], "", []]
      ]
    }
      
    valid_data_list = [2.0, 3.0, 4.0, 5.0]
    invalid_data_list = [1.0, 1.5, 0, -1.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_num_max_inclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["x5"], "", []]
      ]
    }
      
    valid_data_list = [-1.0, 0.0, 1.0, 2.0, 3.5]
    invalid_data_list = [6.0, 100.5, 1000.0, 10000.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_num_min_exclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["y5"], "", []]
      ]
    }
      
    valid_data_list = [6.0, 100.5, 1000.0, 10000.0]  
    invalid_data_list = [1.0, 1.5, 0, -1.0, 5.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_num_max_exclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["x5"], "", []]
      ]
    }
    
    valid_data_list = [-1.0, 0.0, 1.0, 2.0, 3.5]
    invalid_data_list = [6.0, 100.5, 1000.0, 10000.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)         