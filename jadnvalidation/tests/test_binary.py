from jadnvalidation.tests.test_utils import validate_valid_data, validate_invalid_data


def test_binary():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", [], "", []]
      ]
    }
    
    valid_bytes_1 = b"this is a test"
    valid_bytes_2 = b'\x80\x81\x82'
    valid_bytes_3 = "this is a test"
    invalid_bytes_1 = bytearray("hello", "utf-16")
    
    valid_data_list = [valid_bytes_1, valid_bytes_2, valid_bytes_3]
    invalid_data_list = [invalid_bytes_1]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_min():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["{2"], "", []]
      ]
    }
    
    bytes_valid_1 = b"this is a test"
    bytes_valid_2 = b'\x80\x81\x82'
    bytes_invalid_1 = b"x"
    bytes_invalid_2 = bytearray("hello", "utf-16")
    bytes_invalid_3 = b'\x80'
    
    valid_data_list = [bytes_valid_1, bytes_valid_2]
    invalid_data_list = [bytes_invalid_1, bytes_invalid_2, bytes_invalid_3]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_min_max():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["{4","}8"], "", []]
      ]
    }
    
    bytes_valid_1 = b"test"
    bytes_valid_2 = b'\x80\x81\x82\x82'
    bytes_invalid_1 = b"zzzzzzzzzzz"
    bytes_invalid_2 = bytearray("hello", "utf-16")
    bytes_invalid_3 = b'\x80\x80\x80\x80\x80\x80\x80\x80\x80'
    
    valid_data_list = [bytes_valid_1, bytes_valid_2]
    invalid_data_list = [bytes_invalid_1, bytes_invalid_2, bytes_invalid_3]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_eui():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/eui"], "", []]
      ]
    }
    
    bytes_valid_1 = "00:00:5e:00:53:01"
    bytes_valid_2 = b"00:00:5e:00:53:01"
    bytes_invalid_1 = b"zzzz"
    bytes_invalid_2 = "zzzz"
    valid_data_list = [bytes_valid_1, bytes_valid_2]
    invalid_data_list = [bytes_invalid_1, bytes_invalid_2]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_ipv4_addr(): 
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/ipv4-addr"], "", []]
      ]
    }  
    
    valid_data_list = ["127.0.0.1"]
    invalid_data_list = ["zz127.0.0.1zz"]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_ipv6_addr(): 
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/ipv6-addr"], "", []]
      ]
    }  
    
    valid_data_list = ["2001:db8:3333:4444:5555:6666:1.2.3.4"]
    invalid_data_list = ["http://www.example.com"]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)