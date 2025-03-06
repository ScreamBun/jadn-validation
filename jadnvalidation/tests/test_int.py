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

# TODO: Leftoff here
def test_type_int_i8():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", ["/i8"], ""]
      ]
    }
      
    i8_instance_data_1 = {'Integer-Instance': 1}
    i8_instance_data_2 = {'Integer-Instance': 0}
    i8_instance_data_invalid_1 = {'Integer-Instance': 5555}
    i8_instance_data_invalid_2 = {'Integer-Instance': -3333}  
    i8_instance_data_invalid_3 = {'Integer-Instance': "twelve-teen"}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)  

    try:
        pyd_model.model_validate(i8_instance_data_1)
        pyd_model.model_validate(i8_instance_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0  
    
    try:
        pyd_model.model_validate(i8_instance_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(i8_instance_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
    try:
        pyd_model.model_validate(i8_instance_data_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 3
    
def test_type_int_i16():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", ["/i16"], ""]
      ]
    }
      
    i16_instance_data_1 = {'Integer-Instance': 1}
    i16_instance_data_2 = {'Integer-Instance': 0}
    i16_instance_data_invalid_1 = {'Integer-Instance': 555555}
    i16_instance_data_invalid_2 = {'Integer-Instance': -333333}  
    i16_instance_data_invalid_3 = {'Integer-Instance': "thirteen-teen"}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)

    try:
        pyd_model.model_validate(i16_instance_data_1)
        pyd_model.model_validate(i16_instance_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0  
    
    try:
        pyd_model.model_validate(i16_instance_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(i16_instance_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
    try:
        pyd_model.model_validate(i16_instance_data_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 3
    
def test_type_int_i32():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", ["/i32"], ""]
      ]
    }
      
    i32_instance_data_1 = {'Integer-Instance': 1}
    i32_instance_data_2 = {'Integer-Instance': 0}
    i32_instance_data_invalid_1 = {'Integer-Instance': 5555555555}
    i32_instance_data_invalid_2 = {'Integer-Instance': -3333333333}  
    i32_instance_data_invalid_3 = {'Integer-Instance': "a dozen dozen, aka a gross"}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)

    try:
        pyd_model.model_validate(i32_instance_data_1)
        pyd_model.model_validate(i32_instance_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0  
    
    try:
        pyd_model.model_validate(i32_instance_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(i32_instance_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
    try:
        pyd_model.model_validate(i32_instance_data_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 3

def test_type_int_uN():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", ["/u2"], ""]
      ]
    }
      
    uN_instance_data_1 = {'Integer-Instance': 1}
    uN_instance_data_2 = {'Integer-Instance': 0}
    uN_instance_data_3 = {'Integer-Instance': 3}
    uN_instance_data_invalid_1 = {'Integer-Instance': 5}
    uN_instance_data_invalid_2 = {'Integer-Instance': -1}  
    uN_instance_data_invalid_3 = {'Integer-Instance': "pi"}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)

    try:
        pyd_model.model_validate(uN_instance_data_1)
        pyd_model.model_validate(uN_instance_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0  

    try:
        pyd_model.model_validate(uN_instance_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0  
    
    try:
        pyd_model.model_validate(uN_instance_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(uN_instance_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
    try:
        pyd_model.model_validate(uN_instance_data_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 3