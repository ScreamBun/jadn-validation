import datetime
import pprint
from pydantic import ValidationError, create_model
from jadnvalidation.models.jadn.jadn import Config, Info, Jadn
from jadnvalidation.utils import split_on_first_char
from pydantic_schema import build_pyd_fields


def test_string_pattern():
  
    jadn_string_pattern = {
      "types": [
        ["String-Pattern", "String", ["%^jarvis$"], ""]
      ]
    }

    string_pattern_data_1 = {'String-Pattern': 'jarvis'}
    string_pattern_data_invalid_1 = {'String-Pattern': 'JARVIS'}
    string_pattern_data_invalid_2 = {'String-Pattern': 'zzjarviszz'}  
  
    error_count = 0
    try:
        user_custom_fields = build_pyd_fields(jadn_string_pattern)
        
        custom_jadn_schema = create_model(
            "custom_jadn_schema", 
            # __base__= BaseLearnerNode, 
            **user_custom_fields
        )
        
        custom_jadn_schema.model_validate(string_pattern_data_1)   
        
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    assert error_count == 0  
    
    try:
        custom_jadn_schema.model_validate(string_pattern_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_jadn_schema.model_validate(string_pattern_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 2

def test_string_datetime():
  
    jadn_string_datetime = {
      "types": [
        ["String-Datetime", "String", ["/date-time"], ""]
      ]
    }

    string_datatime_data_1 = {'String-Datetime': '2024-01-01'}
    string_datatime_data_2 = {'String-Datetime': datetime.datetime.now()}
    string_datatime_data_3 = {'String-Datetime': 1596542285000}
    string_datatime_data_invalid_1 = {'String-Datetime': 'hfdkjlajfdkl'}
    string_datatime_data_invalid_2 = {'String-Datetime': 'yy2024-01-01zz'}  
  
    error_count = 0
    try:
        user_custom_fields = build_pyd_fields(jadn_string_datetime)
        
        custom_jadn_schema = create_model(
            "custom_jadn_schema", 
            # __base__= BaseLearnerNode, 
            **user_custom_fields
        )
        
        custom_jadn_schema.model_validate(string_datatime_data_1)   
        custom_jadn_schema.model_validate(string_datatime_data_2)
        custom_jadn_schema.model_validate(string_datatime_data_3)
        
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    assert error_count == 0
    
    try:
        custom_jadn_schema.model_validate(string_datatime_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_jadn_schema.model_validate(string_datatime_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 2
  

def test_jadn_str():
  
    jadn_string = {
      "types": [
        ["String-Type", "String", ["{4", "}12"], ""]
      ]
    }

    string_data = {'String-Type': 'test string'}
    string_data_invalid_1 = {'String-Type': 4323 }
    string_data_invalid_2 = {'String-Type': 'zz' }
    string_data_invalid_3 = {'String-Type': 'testing string' }  
  
    error_count = 0
    try:
        user_custom_fields = build_pyd_fields(jadn_string)
        
        custom_jadn_schema = create_model(
            "custom_jadn_schema", 
            # __base__= BaseLearnerNode, 
            **user_custom_fields
        )
        
        custom_jadn_schema.model_validate(string_data)   
        
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 0        
        
    try:
        custom_jadn_schema.model_validate(string_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_jadn_schema.model_validate(string_data_invalid_2)      
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_jadn_schema.model_validate(string_data_invalid_3)      
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 3
  

def test_theory():
  
    simple_jadn = {
      "info": {
        "package": "http://test/v1.0",
        "exports": []
      },
      "types": [
        ["String-Type", "String", [], "string description"],
        ["Number-Type", "Number", [], "number description"],
        ["Integer-Type", "Integer", [], "integer description"],
        ["Boolean-Type", "Boolean", [], "boolean description"]
      ]
    }
    
    test_jadn_data = { 
                      'String-Type': 'test string', 
                      'Number-Type': 123.50,
                      'Integer-Type': 123,
                      'Boolean-Type': True
                      }

    test_jadn_data_invalid = { 
                              'String-Type': 'test string', 
                              'Number-Type': 123.50,
                              'Integer-Type': 'fdasdsaf',
                              'Boolean-Type': True
                            }    
  
    try:
        user_custom_fields = build_pyd_fields(simple_jadn)
        
        custom_jadn_schema = create_model(
            "custom_jadn_schema", 
            # __base__= BaseLearnerNode, 
            **user_custom_fields
        )
        
        custom_jadn_schema.model_validate(test_jadn_data)   
        custom_jadn_schema.model_validate(test_jadn_data_invalid)  
        
    except ValidationError as e:
        print(e)
        
        
def test_get_type_opt_id_val():
  test_opt_1 = "{4"
  opt_char_id, opt_val = split_on_first_char(test_opt_1)
  assert opt_char_id == "{"
  assert opt_val == "4"
  
  test_opt_2 = "}3" 
  opt_char_id, opt_val = split_on_first_char(test_opt_2)
  assert opt_char_id == "}"
  assert opt_val == "3"
  
  test_opt_4 = "/date-time"
  opt_char_id, opt_val = split_on_first_char(test_opt_4)
  assert opt_char_id == "/"
  assert opt_val == "date-time"
  
  test_opt_5 = "%[0-9]"
  opt_char_id, opt_val = split_on_first_char(test_opt_5)
  assert opt_char_id == "%"
  assert opt_val == "[0-9]"   


def test_jadn():
    
    try:
        config = Config()
        info = Info(package="http://www.example.com", config=config)
        jadn = Jadn(info=info)
        jadn_json = jadn.model_dump_json(indent=4)
        pprint.pprint(jadn_json)
    except ValidationError as e:
        print(e)