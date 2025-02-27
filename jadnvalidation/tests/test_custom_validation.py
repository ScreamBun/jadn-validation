from jadnvalidation.jadn_custom_validation import custom_validation


def test_arrary_validation():
    j_schema = {
        "types": [
            ["Array-Test", "Array", ["{3", "}3"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            { "Array-Test": ["test", True, 123] },
        ]  
    
    invalid_data_list = [
            { "Array-Test": ["test", True] },
            { "Array-Test": "test" },
            { "Array-Test": ["test", "test", "test", 123, "test", "test", False] }
        ]        
    
    try :
        for data in valid_data_list:
            custom_validation(j_schema, data)
    except Exception as err:
        print(err)
        assert False     
                
    err_count = 0                
    for data in invalid_data_list:
        try :
            custom_validation(j_schema, data)
        except Exception as err:
            print(err)
            err_count += 1
    
    assert len(invalid_data_list) == err_count