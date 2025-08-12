from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_string_field_multiplicity():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}10"], "", [
                [1, "field_value_1", "String", ["]1"], ""],
                [2, "field_value_2", "String", ["[0"], ""],
                [2, "field_value_3", "String", ["]3"], ""]
            ]]          
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1": "darth mekhis",
            "field_value_2": "darth bane",
            "field_value_3": ["darth nihilus", "darth malgus", "darth revan"]
        },
        {
            "field_value_1": "darth mekhis",
            "field_value_3": ["darth nihilus", "darth malgus", "darth revan"]
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "test 2",
            "field_value_3": ["darth nihilus", "darth malgus", "darth revan", "darth mekhis"]
        }
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    

def test_int_field_multiplicity():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}10"], "", [
                [1, "field_value_1", "String", ["]1"], ""],
                [2, "field_value_2", "String", ["[0"], ""],
                [2, "field_value_3", "Integer", ["]3"], ""]
            ]]          
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1": "darth mekhis",
            "field_value_2": "darth bane",
            "field_value_3": [1, 2, 3]
        },
        {
            "field_value_1": "darth mekhis",
            "field_value_3": [1, 11, 111]
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "test 2",
            "field_value_3": [1, 11, 111, 1111]
        }
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    
    
    
def test_ref_int_field_multiplicity():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}10"], "", [
                [1, "field_value_1", "String", ["]1"], ""],
                [2, "field_value_2", "String", ["[0"], ""],
                [2, "field_value_3", "RefInteger", ["]3"], ""]
            ]],
            ["RefInteger", "Integer", [], "", []]
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1": "darth mekhis",
            "field_value_2": "darth bane",
            "field_value_3": [1, 2, 3]
        },
        {
            "field_value_1": "darth mekhis",
            "field_value_3": [1, 11, 111]
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "test 2",
            "field_value_3": [[1], [11], [111], [1111]]
        }
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_ref_array_field_multiplicity():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}10"], "", [
                [1, "field_value_1", "String", ["]1"], ""],
                [2, "field_value_2", "String", ["[0"], ""],
                [2, "field_value_3", "RefArray", ["]3"], ""]
            ]],
            ["RefArray", "Array", [], "", [
                [1, "field_value_1", "String", [], ""]
            ]]
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1": "darth mekhis",
            "field_value_2": "darth bane",
            "field_value_3": [["darth nihilus"], ["darth malgus"], ["darth revan"]]
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "test 2",
            "field_value_3": [["darth nihilus"], ["darth malgus"], ["darth revan"], ["darth mekhis"]]
        }
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_ref_array_of_field_multiplicity():
    root = "Root-Test"
    
    j_schema =   {  
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1a", "String", [], ""],
                [2, "field_value_1b", "ArrayName2", ["]4"], ""]
            ]],
            ["ArrayName2", "ArrayOf", ["*String"], ""]
        ]
    }
    
    valid_data_list = [
            ['Any String', [["AnyString2"]]],
            ['123', [['HelloWorld', 'this', 'is', 'Strings']]]
        ]
    
    invalid_data_list = [
            [[123, 'Any String']],
            [True], [['Hi im one item']]
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)    