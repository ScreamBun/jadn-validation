import pprint
from pydantic import ValidationError, create_model
from jadnvalidation.models.jadn.jadn import Config, Info, Jadn
from jadnvalidation.utils import split_on_first_char
from pydantic_schema import build_pyd_fields


def test_type_num():
  
    jadn_number_instance = {
      "types": [
        ["Number-Instance", "Number", [], ""]
      ]
    }
      
    number_instance_data_1 = {'Number-Instance': 1.5}
    number_instance_data_invalid_1 = {'Number-Instance': "1.7zz5"}
    number_instance_data_invalid_2 = {'Number-Instance': "0.0.0.0.0.0.0.0.1.2"}  
    number_instance_data_invalid_3 = {'Number-Instance': 5+3j}  
  
    error_count = 0
    try:
        user_custom_fields = build_pyd_fields(jadn_number_instance)
        
        custom_jadn_schema = create_model(
            "custom_jadn_schema", 
            # __base__= BaseLearnerNode, 
            **user_custom_fields
        )
        
        custom_jadn_schema.model_validate(number_instance_data_1)   
        
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    assert error_count == 0  
    
    try:
        custom_jadn_schema.model_validate(number_instance_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_jadn_schema.model_validate(number_instance_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    try:
        custom_jadn_schema.model_validate(number_instance_data_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  

    assert error_count == 3