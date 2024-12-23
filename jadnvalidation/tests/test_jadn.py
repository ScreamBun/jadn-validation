import datetime
import pprint
from pydantic import ValidationError, create_model
from jadnvalidation.models.jadn.jadn import Config, Info, Jadn
from jadnvalidation.models.utils.general_utils import split_on_first_char
from pydantic_schema import build_pyd_fields


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
        
def test_jadn():
    
    try:
        config = Config()
        info = Info(package="http://www.example.com", config=config)
        jadn = Jadn(info=info)
        jadn_json = jadn.model_dump_json(indent=4)
        pprint.pprint(jadn_json)
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
