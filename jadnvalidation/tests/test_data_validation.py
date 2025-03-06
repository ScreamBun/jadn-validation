from jadnvalidation.data_validation.data_validation import DataValidation


def test_data_validation():  
    root = "Array-Test"
    
    j_schema = {
        "types": [
            ["Array-Test", "Array", ["{3", "}3"], "", [
                [1, "field_value_1", "String", ["{2"], ""],
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
            { "Array-Test": ["t", "test", "test", 123, "test", "test", False] }
        ]        
    
    err_count = 0
    for data in valid_data_list:
        try :
            j_validation = DataValidation(j_schema, root, data)
            j_validation.validate()
        except Exception as err:
            print(err)
            err_count += 1
            
    assert err_count == 0            
                  
    for data in invalid_data_list:
        try :
            j_validation = DataValidation(j_schema, root, data)
            j_validation.validate()
        except Exception as err:
            print(err)
            err_count += 1
    
    assert len(invalid_data_list) == err_count  