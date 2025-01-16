from __future__ import annotations
from typing import List
from pydantic import Field, ValidationError, create_model
from jadnvalidation.models.pyd.schema import Schema
from jadnvalidation.models.pyd.structures import Record
from jadnvalidation.pydantic_schema import create_pyd_model


def test_nested_static_models():

    Person = create_model(
        "Person",
        name=(str, ...),  # Required field
        age=(int, ...),
        address=('Address', ...),  # Nested model field
        model_opts=(str, Field(default="testing model opts", exclude=True, evaluate=False)),
        global_opts=(str, Field(default="testing global opts", exclude=True, evaluate=False)),
        __base__=Record
    ) 
    
    Address = create_model(
        "Address",
        house_number=(str, ...),
        street_name=(str, ...),
        city=(str, ...),
        zip_code=(str, ...),
        model_opts=(str, Field(default="testing model opts", exclude=True, evaluate=False)),
        global_opts=(str, Field(default="testing global opts", exclude=True, evaluate=False)),
        __base__=Record
    )
    
    valid_data = {
        "name" : "roberts",
        "age" : 100,
        "address" : {
            "house_number" : "8888",
            "street_name" : "bats lane",
            "city" : "gotham",
            "zip_code" : "22222",
        }
    }
    
    invalid_data = {
        "name" : "roberts",
        "age" : 100,
        "address" : {
            "house_number" : True,
            "street_name" : "bats lane",
            "city" : "gotham",
            "zip_code" : "22222",
        }
    }     
    
    err_count = 0
    try :
        Person.model_validate(valid_data)    
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        Person.model_validate(invalid_data)    
    except Exception as err:
        err_count = err_count + 1
        print(err)        
               
    assert err_count == 1  
      

def test_forward_refs_experimental():
    Foo = create_model("Foo", foo=(List["RecordName2"], Field(...)))
    Foo_core_schema = Foo.__pydantic_core_schema__
    
    RecordName2 = create_model("RecordName2", bar=(int, Field(...)))
    
    Foo.model_rebuild()
    RecordName2.model_rebuild()
    
    try :
        foo = Foo(foo=[RecordName2(bar=1), RecordName2(bar=2)])
        print(foo)
    except Exception as err:
        print(err)    


def test_forward_ref():
    
    j_schema =   {
        "types": [
            ["RecordName1", "Record", [], "", [
                [1, "field_value_1a", "RecordName2", [], ""]
            ]],
            ["RecordName2", "Record", [], "", [
                [1, "field_value_2a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_1 = {
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2a': 'Anytown'
        }             
    }
    
    invalid_data_1 = {
        'RecordName1': {
            'field_value_1a': {
                'field_value_2a': 'Anytown'
            }  
        },
        'RecordName2': {
            'field_value_2zzzz': False
        }             
    }    
    
    err_count = 0
    custom_schema = {}
    try :
        custom_schema = Schema(**j_schema)
        custom_schema.model_rebuild()
    except Exception as err:
        err_count = err_count + 1
        print(err)    
    
    try :
        custom_schema.model_validate(valid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    try :
        custom_schema.model_validate(invalid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)        
        
    assert err_count == 1

def test_records():
    
    j_schema = {
        "types": [
            ["Record-Name1", "Record", ["{1", "}2"], "", [
                [1, "field_value_1a", "String", [], ""],
                [2, "field_value_2a", "String", [], ""]
            ]],
            ["Record-Name2", "Record", ["{1", "}2"], "", [
                [1, "field_value_1b", "String", [], ""],
                [2, "field_value_2b", "String", [], ""]
            ]]            
        ]
    }  
    
    valid_data_1 = {
        'Record-Name1': {
            'field_value_1a': "test field",
            'field_value_2a': 'Anytown'
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': 'Anytown'
        }        
    }
      
    # valid_data_2 = {
    #     'field_value_1': "test field",
    #     'field_value_2': 'Anytown'
    # }
    
    invalid_data_1 = {
        'Record-Name1': {
            'field_value_1a': True,
            'field_value_2a': 'Anytown'
        },
        'Record-Name2': {
            'field_value_1b': "test field",
            'field_value_2b': False
        }        
    }
    
    err_count = 0
    custom_schema = {}
    try :
        custom_schema = create_pyd_model(j_schema)
        # custom_schema.model_rebuild()
    except Exception as err:
        err_count = err_count + 1
        print(err)    
    
    try :
        custom_schema.model_validate(valid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)
        
    # try :
    #     custom_schema.model_validate(valid_data_2)
    # except Exception as err:
    #     err_count = err_count + 1
    #     print(err)        
        
    try :
        custom_schema.model_validate(invalid_data_1)
    except Exception as err:
        err_count = err_count + 1
        print(err)        
               
    assert err_count == 1
    
        

# TODO: Schema initialization is broken            
def test_record_legacy_initialization(): 
    
    j_schema = {
        "types": [
            ["RecordName", "Record", ["{1", "}2"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }   
    
    data_1 = {
        'RecordName': {
            'field_value_1': "test field",
            'field_value_2': 'Anytown'
        }
    }
    
    data_2 = {
            'field_value_1': "test field",
            'field_value_2': 'Anytown'
    }    
    
    data_invalid_1 = {
        'RecordName': {
            'field_value_1': 123,
            'field_value_2': 'Anytown'
        }
    }    
    
    data_invalid_2 = {
        'field_value_1': 123,
        'field_value_2': 'Anytown'
    }     
    
    custom_model = None    
    error_count = 0
    
    try:
        # custom_model = Schema.model_validate(j_schema)
        custom_model = Schema(**j_schema) 
        custom_model.model_rebuild()
        print(custom_model)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
    
    try:
        custom_model.model_validate(data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_model.model_validate(data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
    
    try:
        custom_model.model_validate(data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        custom_model.model_validate(data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    assert error_count == 1
