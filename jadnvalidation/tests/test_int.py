from pydantic import ValidationError
from jadnvalidation.tests.test_utils import validate_valid_data
from pydantic_schema import create_pyd_model


def test_type_int():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", [], ""]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

# TODO: Add duration formatting?
def test_type_int_duration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", [], ""]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_min():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["{2"], ""]
      ]
    }
      
    valid_data_list = [3, 55]      
    invalid_data_list = [1, 0, -1]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_max():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["}2"], ""]
      ]
    }
      
    valid_data_list = [-1, 2]      
    invalid_data_list = [3, 5] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_i8():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i8"], ""]
      ]
    }
    
    valid_data_list = [0, 1]      
    invalid_data_list = [5555, -3333, "thirteen-teen"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_int_i16():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i16"], ""]
      ]
    }
    
    valid_data_list = [0, 1]      
    invalid_data_list = [555555, -333333, "four-teen"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_int_i32():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i32"], ""]
      ]
    }
    
    valid_data_list = [0, 1]      
    invalid_data_list = [5555555555, -3333333333, "dozen dozen"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)