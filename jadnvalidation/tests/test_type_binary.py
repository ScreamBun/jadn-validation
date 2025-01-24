from pydantic import ValidationError
from jadnvalidation.pydantic_schema import create_pyd_model


def test_binary():
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", [], ""]
      ]
    }
    
    bytes_1 = b"this is a test"
    bytes_valid_2 = b'\x80\x81\x82'
    bytes_invalid_2 = bytearray("hello", "utf-16")
    
    valid_data_1 = {'Binary-Test': bytes_1}
    valid_data_2 = {'Binary-Test': bytes_valid_2}
    invalid_data_2 = {'Binary-Test': bytes_invalid_2}
    
    error_count = 0
    try:
        pyd_model = create_pyd_model(jadn_schema)    
        print(pyd_model)
    except Exception as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                                         
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0         
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1
    
def test_binary_min():
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", ["{2"], ""]
      ]
    }
    
    bytes_1 = b"this is a test"
    bytes_valid_2 = b'\x80\x81\x82'
    bytes_invalid_1 = b"x"
    bytes_invalid_2 = bytearray("hello", "utf-16")
    bytes_invalid_3 = b'\x80'
    
    valid_data_1 = {'Binary-Test': bytes_1}
    valid_data_2 = {'Binary-Test': bytes_valid_2}
    invalid_data_1 = {'Binary-Test': bytes_invalid_1}
    invalid_data_2 = {'Binary-Test': bytes_invalid_2}
    invalid_data_3 = {'Binary-Test': bytes_invalid_3}
    
    error_count = 0
    try:
        pyd_model = create_pyd_model(jadn_schema)    
        print(pyd_model)
    except Exception as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                      
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                
        
    assert error_count == 3
    
def test_binary_max():
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", ["}4"], ""]
      ]
    }
    
    bytes_1 = b"test"
    bytes_valid_2 = b'\x80\x81\x82'
    bytes_invalid_1 = b"zzzzzz"
    bytes_invalid_2 = bytearray("hello", "utf-16")
    bytes_invalid_3 = b'\x80\x80\x80\x80\x80\x80'
    
    valid_data_1 = {'Binary-Test': bytes_1}
    valid_data_2 = {'Binary-Test': bytes_valid_2}
    invalid_data_1 = {'Binary-Test': bytes_invalid_1}
    invalid_data_2 = {'Binary-Test': bytes_invalid_2}
    invalid_data_3 = {'Binary-Test': bytes_invalid_3}
    
    error_count = 0
    try:
        pyd_model = create_pyd_model(jadn_schema)    
        print(pyd_model)
    except Exception as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                      
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                
        
    assert error_count == 3
    
def test_binary_min_max():
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", ["{4","}8"], ""]
      ]
    }
    
    bytes_1 = b"test"
    bytes_valid_2 = b'\x80\x81\x82\x82'
    bytes_invalid_1 = b"zzzzzzzzzzz"
    bytes_invalid_2 = bytearray("hello", "utf-16")
    bytes_invalid_3 = b'\x80\x80\x80\x80\x80\x80\x80\x80\x80'
    
    valid_data_1 = {'Binary-Test': bytes_1}
    valid_data_2 = {'Binary-Test': bytes_valid_2}
    invalid_data_1 = {'Binary-Test': bytes_invalid_1}
    invalid_data_2 = {'Binary-Test': bytes_invalid_2}
    invalid_data_3 = {'Binary-Test': bytes_invalid_3}
    
    error_count = 0
    pyd_model = {}
    try:
        pyd_model = create_pyd_model(jadn_schema)    
        print(pyd_model)
    except Exception as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                      
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                
        
    assert error_count == 3
    
def test_binary_eui(): 
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", ["/eui"], ""]
      ]
    }  
    
    valid_data_1 = {'Binary-Test': "00:00:5e:00:53:01"}
    invalid_data_1 = {'Binary-Test': "zzzz"}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                                        
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)               
        
    assert error_count == 1
    
def test_binary_ipv4_addr(): 
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", ["/ipv4-addr"], ""]
      ]
    }  
    
    valid_data_1 = {'Binary-Test': "127.0.0.1"}
    invalid_data_1 = {'Binary-Test': "zz127.0.0.1zz"}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                                        
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)               
        
    assert error_count == 1
    
def test_binary_ipv6_addr(): 
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", ["/ipv6-addr"], ""]
      ]
    }  
    
    valid_data_1 = {'Binary-Test': "2001:db8:3333:4444:5555:6666:1.2.3.4"}
    invalid_data_1 = {'Binary-Test': "http://www.example.com"}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                                        
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)               
        
    assert error_count == 1     