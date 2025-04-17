from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_map_of_int_string():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Integer-Name", "Integer", [], ""],
            ["String-Name", "String", [], ""],
            ["Root-Test", "MapOf", ["+Integer", "*String"], ""]
        ]
    }
    
    valid_data_list = [
         [1, "asdf", 2, "fdsaf"]
    ]
    
    invalid_data_list = [
         [1, True, 2, False]
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_map_of_int_string():
    # TODO: Need to add key or id attributes to XML data and logic to validate it
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Integer-Name", "Integer", [], ""],
            ["String-Name", "String", [], ""],
            ["Root-Test", "MapOf", ["+Integer", "*String"], ""]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <1>val1</1>
        <2>val2</2>
        <3>val3</3>
    </Root-Test>"""  
    
    invalid_xml_1 = """<Root-Test>
        <1>True</1>
        <2>False</2>
        <3>0</3>
    </Root-Test>"""    
    
    valid_data_list = [
        valid_xml_1
    ]
    
    invalid_data_list = [
        invalid_xml_1
    ]
    
    # err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    # assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)    
    
def test_map_of_string_string():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["String-Name", "String", [], ""],
            ["Root-Test", "MapOf", ["+String", "*String"], ""]
        ]
    }
    
    valid_data_list = [

                {
                    "key1" : "val1",
                    "key2" : "val2",
                    "key3" : "val3"
                }       

    ]
    
    invalid_data_list = [
                {
                    1 : "val1",
                    "key2" : 2,
                    "key3" : True
                }
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)  
    
def test_xml_map_of_string_string():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "MapOf", ["+String", "*String"], ""]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <key1>val1</key1>
        <key2>val2</key2>
        <key3>val3</key3>
    </Root-Test>"""  
    
    invalid_xml_1 = """<Root-Test>
        <1>val1</1>
        <key2>2</key2>
        <key3>True</key3>
    </Root-Test>"""    
    
    valid_data_list = [
        valid_xml_1
    ]
    
    invalid_data_list = [
        invalid_xml_1
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)         