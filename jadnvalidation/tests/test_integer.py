from jadnvalidation.tests.test_utils import validate_valid_data, validate_invalid_data
from jadnvalidation.utils.consts import XML


def test_type_int():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", [], "", []]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_type_int():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", [], "", []]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    valid_xml_1 = """<Root-Test>1</Root-Test>"""
    valid_xml_2 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

# TODO: Add duration formatting?
def test_type_int_duration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", [], "", []]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_min():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["{2"], "", []]
      ]
    }
      
    valid_data_list = [3, 55]      
    invalid_data_list = [1, 0, -1]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_max():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["}2"], "", []]
      ]
    }
      
    valid_data_list = [1, 2]      
    invalid_data_list = [3, 5] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_i8():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i8"], "", []]
      ]
    }
    
    valid_data_list = [0, 1]      
    invalid_data_list = [5555, -3333, "thirteen-teen"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_int_i16():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i16"], "", []]
      ]
    }
    
    valid_data_list = [0, 1]      
    invalid_data_list = [555555, -333333, "four-teen"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_int_i32():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i32"], "", []]
      ]
    }
    
    valid_data_list = [0, 1]      
    invalid_data_list = [5555555555, -3333333333, "dozen dozen"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)