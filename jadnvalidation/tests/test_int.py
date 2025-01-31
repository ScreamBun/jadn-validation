from pydantic import ValidationError
from pydantic_schema import create_pyd_model


def test_type_int():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", [], ""]
      ]
    }
      
    integer_instance_data_1 = {'Integer-Instance': 1}
    integer_instance_data_2 = {'Integer-Instance': 0}
    integer_instance_data_invalid_1 = {'Integer-Instance': 1.75}
    integer_instance_data_invalid_2 = {'Integer-Instance': "one"}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(integer_instance_data_1)
        pyd_model.model_validate(integer_instance_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0
    
    try:
        pyd_model.model_validate(integer_instance_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(integer_instance_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 2


def test_type_int_duration():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", [], ""]
      ]
    }
      
    integer_instance_data_duration_1 = {'Integer-Instance': 1000}
    integer_instance_data_duration_2 = {'Integer-Instance': 0}
    integer_instance_data_invalid_duration_1 = {'Integer-Instance': 1.75}
    integer_instance_data_invalid_duration_2 = {'Integer-Instance': "one-minute"}  
    integer_instance_data_invalid_duration_3 = {'Integer-Instance': "-5000"}
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(integer_instance_data_duration_1)
        pyd_model.model_validate(integer_instance_data_duration_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0 
    
    try:
        pyd_model.model_validate(integer_instance_data_invalid_duration_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(integer_instance_data_invalid_duration_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    try:
        pyd_model.model_validate(integer_instance_data_invalid_duration_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 3

def test_type_int_min():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", ["{1"], ""]
      ]
    }
      
    integer_instance_data_min_1 = {'Integer-Instance': 1}
    integer_instance_data_min_2 = {'Integer-Instance': 55}
    integer_instance_data_invalid_min_1 = {'Integer-Instance': -1}
    integer_instance_data_invalid_min_2 = {'Integer-Instance': 1.75}
    integer_instance_data_invalid_min_3 = {'Integer-Instance': "one"}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model) 
        
    assert error_count == 0  
    
    try:
        pyd_model.model_validate(integer_instance_data_min_1)
        pyd_model.model_validate(integer_instance_data_min_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0  

    try:
        pyd_model.model_validate(integer_instance_data_invalid_min_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(integer_instance_data_invalid_min_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)

    try:
        pyd_model.model_validate(integer_instance_data_invalid_min_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)

    assert error_count == 3

def test_type_int_max():
  
    jadn_schema = {
      "types": [
        ["Integer-Instance", "Integer", ["}1"], ""]
      ]
    }
      
    integer_instance_data_max_1 = {'Integer-Instance': 1}
    integer_instance_data_max_2 = {'Integer-Instance': -3}
    integer_instance_data_invalid_max_1 = {'Integer-Instance': 77}
    integer_instance_data_invalid_max_2 = {'Integer-Instance': 1.75}
    integer_instance_data_invalid_max_3 = {'Integer-Instance': "one"}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model) 
    
    try:
        pyd_model.model_validate(integer_instance_data_max_1)
        pyd_model.model_validate(integer_instance_data_max_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0  

    try:
        pyd_model.model_validate(integer_instance_data_invalid_max_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(integer_instance_data_invalid_max_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)

    try:
        pyd_model.model_validate(integer_instance_data_invalid_max_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)

    assert error_count == 3

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