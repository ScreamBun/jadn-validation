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
        ["Root-Test", "Integer", ["/duration"], "", []]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_day_time_duration():
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

def test_type_int_year_month_duration():
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

def test_type_int_gYear():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gYear"], "", []]
      ]
    }
      
    valid_data_list = [1999, 0000, -1000, "1999", "0000", "-0010", "2025Z", "2024-05:00"]      
    invalid_data_list = [1.75, "one", "1.7z5", 93, 444, "90", "100"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_gYearMonth():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gYearMonth"], "", []]
      ]
    }
      
    valid_data_list = ["1000-12", "-1000-05", "1000-12-05:00", "-1000-05Z"]      
    invalid_data_list = ["one", "1.7z5", 99, 1.750, 1000, "1000", "01-01", "1999-99", ""]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_gMonthDay():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gMonthDay"], "", []]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)