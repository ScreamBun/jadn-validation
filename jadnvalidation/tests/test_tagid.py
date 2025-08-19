from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_jadn_type_test_derived_enumeration():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "type_name", "String", [], ""],
                [2, "core_type", "Core-Types", [], ""],
                [3, "fields", "JADN-Type", ["&2"], ""]
            ]],    
            ["Core-Types", "Enumerated", ["#JADN-Type"], "", []],
            ["JADN-Type", "Choice", [], "", [
                [1, "string", "Array-Empty", [], ""],
                [2, "record", "Array-Fields", [], ""],
                [3, "enum", "Array-Items", [], ""]
            ]],    
            ["Array-Items", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]],
            ["Array-Fields", "Array", [], "", [
                [1, "field_value_a", "String", [], ""],
                [2, "field_value_b", "String", [], ""]
            ]],
            ["Array-Empty", "Array", [], "", []]
        ]
    }
    
    valid_data_list = [
        [
            "my name",
            "string",
            []
        ] 
    ]
    # invalid_data_list = ['redd',2,'test']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    # err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    # assert err_count == len(invalid_data_list)