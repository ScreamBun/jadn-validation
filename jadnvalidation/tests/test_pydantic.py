from model import Model
from person import Person
from pydantic import ValidationError
from uuid import uuid4


def gen_uuid():
    return str(uuid4())
   
def test_person():
    p = Person(first_name = "ace", last_name = "ventura", age = 30)
    assert str(p.first_name) == "ace"
    assert str(p.last_name) == "ventura"
    assert int(p.age) == 30
    
    try:
        p = Person(first_name = "ace", last_name = 100, age = "junk")
    except ValidationError as ex:
        err_msg = ex
        errs = err_msg.errors()
        errs_json = err_msg.json()
        
        err_count = err_msg.error_count()
        assert int(err_count) == 2
        
        print(err_msg)
        
def test_data_deserializing():
    data = {
        "first_name": "Ace",
        "last_name": "Ventura",
        "age": 40
    }
    
    p = Person.model_validate(data)
    assert str(p.first_name) == "Ace"
    assert str(p.last_name) == "Ventura"
    assert int(p.age) == 40
        
    print(p)
    
def test_json_deserializing():
    json_data = '''{
        "first_name": "Mike",
        "last_name": "Myers",
        "age": 20
    }'''
    
    p = Person.model_validate_json(json_data)
    assert str(p.first_name) == "Mike"
    assert str(p.last_name) == "Myers"
    assert int(p.age) == 20    
    print(p)    
    
def test_json_serializing():    
    p = Person(first_name = "ace", last_name = "ventura", age = 30)
    p_dict = p.model_dump()
    print(p_dict)  
    p_dict_alias = p.model_dump(by_alias=True)
    print(p_dict_alias)      
    p_json = p.model_dump_json()
    print(p_json)
    p_json_alias = p.model_dump_json(by_alias=True)
    print(p_json_alias)       
    
def test_optional_required_fields():
    mf = Person.model_fields
    print(mf)
    
    p = Person(first_name="Freddy", last_name="Krueger")
    assert str(p.first_name) == "Freddy"
    assert str(p.last_name) == "Krueger"
    assert int(p.age) == 0    
    
    p.age = 500
    assert int(p.age) == 500  
    
    print(p)
    
def test_field_unique():
    try:
        Model(numbers=["1", 1, "2", 3.0])
    except ValidationError as ex:
        ex_json = ex.json()
        print(ex)
        
    try:
        Model(numbers=["1", "2", 3.0])
    except ValidationError as ex:
        ex_json = ex.json()
        print(ex)        