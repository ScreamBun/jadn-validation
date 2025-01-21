from pydantic import ValidationError
from pydantic_schema import create_pyd_model 


def test_type_num():
  
    jadn_schema = {
      "types": [
        ["NumberInstance", "Number", [], ""]
      ]
    }
      
    number_instance_data_1b = { 'root_model' : {
                                    'NumberInstance': 1.5
                                }
                            }
    number_instance_data_1 = {'NumberInstance': 1.5}
    number_instance_data_invalid_1 = {'NumberInstance': "1.7zz5"}
    number_instance_data_invalid_2 = {'NumberInstance': "0.0.0.0.0.0.0.0.1.2"}  
    number_instance_data_invalid_3 = {'NumberInstance': 5+3j}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(number_instance_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 0  
    
    try:
        pyd_model.model_validate(number_instance_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(number_instance_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    try:
        pyd_model.model_validate(number_instance_data_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 3