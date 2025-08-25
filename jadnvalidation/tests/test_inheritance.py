from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.general_utils import sort_array_by_id


def test_order_array_by_id():
    
    j_feilds_1 =  [
                [1, "item_1", "String", []],
                [2, "item_2", "String", []],
                [3, "item_3", "String", []],
            ]
    
    ordered_array =  sort_array_by_id(j_feilds_1)
    
    assert ordered_array == [
                [1, "item_1", "String", []],
                [2, "item_2", "String", []],
                [3, "item_3", "String", []],
            ]
    
def test_order_arrays_by_id():
    
    j_feilds_1 =  [
                [111, "common_1", "Integer", ["[0"]],
                [222, "common_2", "Integer", ["[0"]],
                [333, "common_3", "Integer", ["[0"]],
            ]
    
    j_feilds_2 =  [
                [1, "item_1", "String", []],
                [2, "item_2", "String", []],
                [3, "item_3", "String", []],
            ]
    
    ordered_array =  sort_array_by_id(j_feilds_1, j_feilds_2)
    
    assert ordered_array == [
                [1, "item_1", "String", []],
                [2, "item_2", "String", []],
                [3, "item_3", "String", []],
                [111, "common_1", "Integer", ["[0"]],
                [222, "common_2", "Integer", ["[0"]],
                [333, "common_3", "Integer", ["[0"]],
            ]
    
def test_invalid_arrays_id():
    
    j_feilds_1 =  [
                [1, "common_1", "Integer", ["[0"]],  # < == DUPLICATE
                [222, "common_2", "Integer", ["[0"]],
                [333, "common_3", "Integer", ["[0"]],
            ]
    
    j_feilds_2 =  [
                [1, "item_1", "String", []], # < == DUPLICATE
                [2, "item_2", "String", []],
                [3, "item_3", "String", []],
            ]
    try:
        ordered_array =  sort_array_by_id(j_feilds_1, j_feilds_2)
    except ValueError as ve:
        assert str(ve) == "Duplicate IDs found in combined array: [1]"
    else:
        assert False, "Expected ValueError for duplicate IDs"

def test_array_inheritance():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Common-Items", "Array", [], "", [
                [1, "common_1", "Integer", ["[0"]],
                [2, "common_2", "Integer", ["[0"]],
                [3, "common_3", "Integer", ["[0"]],
            ]],            
            ["Root-Test", "Array", ["eCommon-Items"], "", [
                [111, "item_1", "String", [], ""],
                [222, "item_2", "String", ["[0"], ""],
                [333, "item_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [1, 2, 3, "item_1", "item_2", "item_3"],
            [None, 2, 3, "item_1", "item_2", "item_3"],
            [1, None, 3, "item_1", "item_2", "item_3"],
            [1, 2, None, "item_1", "item_2", "item_3"],
            [1, 2, 3, "item_1", "", "item_3"],
            [1, 2, 3, "item_1", None, "item_3"],
            [1, 2, 3, "item_1", None],
            [None, None, None, "item_1"],
        ]
    
    invalid_data_list = [
            [1, 2, 3, "item_1", "item_2", "item_3", "extra"],
            [1, 2, 3, 99, "item_1", "item_2", "item_3"],
            [None, 2, 3, None, "item_2", "item_3"],
            [None, None, None, None, None, None],
            [1, 2, 3, 4, 5, 6],
            ["item_1", "item_2", "item_3", "item_4", "item_5", "item_6"],
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)