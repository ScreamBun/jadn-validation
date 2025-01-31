import datetime
import pprint
from pydantic import ValidationError
from jadnvalidation.models.jadn.jadn import Config, Info, Jadn
from jadnvalidation.utils.general_utils import split_on_first_char
from pydantic_schema import create_pyd_model

        
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
