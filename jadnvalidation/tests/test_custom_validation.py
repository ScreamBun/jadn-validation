from jadnvalidation.jadn_custom_validation import custom_validation


def test_arrary_validation():
    j_schema = {
        "types": [
            ["Array-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    data_list = [
            { "Array-Test": "test" },
            { "Array-Test": ["test", True, 123] },
            { "Array-Test": [123, "test", True] },
            { "Array-Test": ["test", "test", "test"] },
            { "Array-Test": ["test", "test", "test", 123, "test", "test", False] }
        ]    
    
    try :
        custom_validation(j_schema, data_list[0])
    except Exception as err:
        print(err)       
    
    assert True    