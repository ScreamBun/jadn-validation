
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_choice():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis"
        }, 
        {
            "field_value_2": False
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_xml_choice():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_1>illum repellendus nobis</field_value_1>
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        <field_value_2>False</field_value_2>
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1>illum repellendus nobis</field_value_1>
        <field_value_2>True</field_value_2>
        <field_value_3>test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x>test incorrect field name</field_value_x>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)
    
def test_choice_id():
    root = "Root-Test"
        
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "1": "illum repellendus nobis",
        }, 
        {
            "2": False
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }       
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_choice_id():
    root = "Root-Test"
        
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_1 key="1">illum repellendus nobis</field_value_1>
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        <field_value_2 id="2">False</field_value_2>
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
        <field_value_3 id="3">test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x key="11">test incorrect field name</field_value_x>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_choice_tagid():
    root = "Root-Test"
        
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "Enum-Example", [], ""],
                [2, "field_value_2", "Choice-Test", ["&1"], ""]
            ]],
            ["Choice-Test", "Choice", [], "", [
                [1, "one", "String", ["%^a$"], ""],
                [2, "two", "String", ["%^b$"], ""]
            ]],
            ["Enum-Example", "Enum", [], "", [
                [1, "one", [], ""],
                [2, "two", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": "one",
            "field_value_2": "a"
        }, 
        {
            "field_value_1": "two",
            "field_value_2": "b"
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }       
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_choice_tagid_2():
    root = "Root-Test"
        
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Type", "Array", [], "", [
                [1, "type_name", "String"],
                [2, "core_type", "Enum-Example"],
                [3, "type_options", "TypeOptions", ["[0", "&2"]]]],
            ["Choice-Test", "Choice", [], "", [
                [1, "one", "String", ["%^a$"], ""],
                [2, "two", "String", ["%^b$"], ""]
            ]],
            ["Enum-Example", "Enum", [], "", [
                [1, "one", [], ""],
                [2, "two", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        ["fieldname", "one", "a"], 
        
        ["fieldname", "two", "b"]
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }       
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_choice_anyOf():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CO"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": False           
        }, 
        {
            "field_value_2": False
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    
        
    
def test_xml_choice_anyOf():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CO"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": False           
        }, 
        {
            "field_value_2": False
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    valid_xml_1 = """<Root-Test>
        <field_value_1 key="1">illum repellendus nobis</field_value_1>
        <field_value_2 key="2">False</field_value_2>
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        <field_value_2 id="2">False</field_value_2>
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
        <field_value_3 id="3">test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x key="11">test incorrect field name</field_value_x>
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>
        <field_value_1 key="1">123</field_value_x>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

    
def test_choice_allOf():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CA"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": False      
        }, 
        {
            "field_value_2": False,
            "field_value_1": "illum repellendus nobis"            
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_xml_choice_allOf():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CA"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_1 key="1">illum repellendus nobis</field_value_1>
        <field_value_2 key="2">False</field_value_2>
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        <field_value_2 id="2">False</field_value_2>
        <field_value_1 key="1">illum repellendus nobis</field_value_1>        
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
        <field_value_3 id="3">test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x key="11">test incorrect field name</field_value_x>
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>
        <field_value_1 key="1">123</field_value_x>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  
    
    
def test_choice_not():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CX"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_a": "illum repellendus nobis",
            "field_value_b": False 
        }, 
        {
            "field_value_b": False,
            "field_value_a": "illum repellendus nobis"            
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True
        }, 
        {
            "field_value_1": "test incorrect field name"
        },
        {
            "field_value_2": False
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_choice_not():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CX"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_a>illum repellendus nobis</field_value_a>
        <field_value_b>False</field_value_b>
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        <field_value_z id="2">False</field_value_z>
        <field_value_y key="1">illum repellendus nobis</field_value_y>  
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_1 key="1">test incorrect field name</field_value_1>
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>
        <field_value_2 key="2">True</field_value_2>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)    

def test_choice_as_field():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Choice-Test", [], ""]
            ]],
            ["Choice-Test", "Choice", [], "", [
                [1, "choice_value_1", "Integer", [], ""],
                [2, "choice_value_2", "Boolean", [], ""]
            ]]
        ]
    }

    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": {"choice_value_1": 1}
        }
    ]

    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }
    ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)  
        

def test_choice_as_field_multiple():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Choice-Test", ["]-1"], ""]
            ]],
            ["Choice-Test", "Choice", [], "", [
                [1, "choice_value_1", "Integer", [], ""],
                [2, "choice_value_2", "Boolean", [], ""]
            ]]
        ]
    }

    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": [{"choice_value_1": 1}, {"choice_value_2": True}]
        }
    ]

    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }
    ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)   