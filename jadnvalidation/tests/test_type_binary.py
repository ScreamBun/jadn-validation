from pydantic import ValidationError, create_model
from jadnvalidation.pydantic_schema import build_pyd_fields


def test_binary():
  
    jadn_schema = {
      "types": [
        ["Binary-Test", "Binary", [], ""]
      ]
    }
    
    bytes_1 = b"this is a test"
    bytes_2 = "this is a test"
    val_string = "Howdy, Partner!"
    bytes_3 = bytearray(val_string, 'utf-8')
    
    # binary_raw_1 = "01101000 01101111 01110000 01100101" # hope
    # hex_1 = convert_binary_to_hex(binary_raw_1)
    
    # binary_raw_2 = "00110001 00111001 00111000 00110100" # 1984
    # hex_2 = convert_binary_to_hex(binary_raw_2)
    
    valid_data_1 = {'Binary-Test': bytes_1}
    valid_data_2 = {'Binary-Test': bytes_2}
    valid_data_3 = {'Binary-Test': bytes_3}
    # invalid_data_1 = {'Binary-Test': 'zzz'}
    # invalid_data_2 = {'Binary-Test': '__false__'}
    
    error_count = 0
    try:
        user_custom_fields = build_pyd_fields(jadn_schema)
        pyd_model = create_model(
            "jadn_schema", 
            **user_custom_fields
        )
    except ValidationError as e:
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
        
    try:
        pyd_model.model_validate(valid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                            
        
    assert error_count == 0        
        
    # try:
    #     pyd_model.model_validate(invalid_data_1)
    # except ValidationError as e:
    #     error_count = error_count + 1
    #     print(e)
        
    # try:
    #     pyd_model.model_validate(invalid_data_2)
    # except ValidationError as e:
    #     error_count = error_count + 1
    #     print(e)            
        
    # assert error_count == 2