import pprint
from pydantic import ValidationError, create_model
from jadnvalidation.models.jadn import Config, Info, Jadn
from pydantic_schema import build_pyd_fields

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

def test_theory():
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
        # err_count = err_count + 1
        print(e)