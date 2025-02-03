import datetime

from jadnvalidation.tests.test_utils import create_testing_model, validate_valid_data


def test_string_regex():
  
    j_schema = {
      "types": [
        ["String-Regex", "String", ["/regex"], ""]
      ]
    }
    
    valid_data_list = [{'String-Regex': '.*ABA.?'},
        {'String-Regex': 'A(BB){1,4}'}]
    invalid_data_list = [{'String-Regex': '['},
        {'String-Regex': '\\'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_relative_json_pointer():
  
    j_schema = {
      "types": [
        ["String-Relative-Json-Pointer", "String", ["/relative-json-pointer"], ""]
      ]
    }
    
    valid_data_list = [{'String-Relative-Json-Pointer': '0/foo'},
        {'String-Relative-Json-Pointer': '1/sin-city'}]
    invalid_data_list = [{'String-Relative-Json-Pointer': '/foo/0'},
        {'String-Relative-Json-Pointer': '-1/sin-city'}]
        
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_json_pointer():
  
    j_schema = {
      "types": [
        ["String-Json-Pointer", "String", ["/json-pointer"], ""]
      ]
    }
    
    valid_data_list = [{'String-Json-Pointer': '/foo'},
        {'String-Json-Pointer': '/foo/0'}]
    invalid_data_list = [{'String-Json-Pointer': 'zzzz'},
        {'String-Json-Pointer': ':///items.starfox'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_iri_ref():
  
    j_schema = {
      "types": [
        ["String-Iri-Reference", "String", ["/iri-reference"], ""]
      ]
    }
    
    valid_data_list = [{'String-Iri-Reference': 'mailto:info@example.com'},
        {'String-Iri-Reference': 'file://localhost/absolute/path/to/file'},
        {'String-Iri-Reference': 'https://www.example.珠宝/'}]
    invalid_data_list = [{'String-Iri-Reference': 'zzzz'},
        {'String-Iri-Reference': ':///items.starfox'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_iri():
  
    j_schema = {
      "types": [
        ["String-Iri", "String", ["/iri"], ""]
      ]
    }
    
    valid_data_list = [{'String-Iri': 'http://puny£code.com'},
        {'String-Iri': 'https://www.аррӏе.com/'},
        {'String-Iri': 'https://www.example.珠宝/'}]
    invalid_data_list = [{'String-Iri': 'zzzz'},
        {'String-Iri': ':///items.starfox'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_uri_template():
  
    j_schema = {
      "types": [
        ["String-Uri-Template", "String", ["/uri-template"], ""]
      ]
    }
    
    valid_data_list = [{'String-Uri-Template': 'https://www.example.com/api/v1/items/{/item_id}'}]
    invalid_data_list = [{'String-Uri-Template': 'zzzz'},
        {'String-Uri-Template': '/items/{}'},
        {'String-Uri-Template': 'https://www.example.com/api/v1/items/'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_uri_ref():
  
    j_schema = {
      "types": [
        ["String-Uri-Ref", "String", ["/uri-reference"], ""]
      ]
    }
    
    valid_data_list = [{'String-Uri-Ref': 'http://www.example.com/questions/3456/my-document'},
        {'String-Uri-Ref': 'mailto:info@example.com'},
        {'String-Uri-Ref': 'file://localhost/absolute/path/to/file'}]
    invalid_data_list = [{'String-Uri-Ref': 'zzzz'},
        {'String-Uri-Ref': '//./file_at_current_dir'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_uri():
  
    j_schema = {
      "types": [
        ["String-Uri", "String", ["/uri"], ""]
      ]
    }
    
    valid_data_list = [{'String-Uri': 'http://www.example.com/questions/3456/my-document'},
        {'String-Uri': 'mailto:info@example.com'},
        {'String-Uri': 'foo://example.com:8042/over/there?name=ferret#nose'}]
    invalid_data_list = [{'String-Uri': 'zzzz'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_ipv6():
  
    j_schema = {
      "types": [
        ["String-Ipv6", "String", ["/ipv6"], ""]
      ]
    }
    
    valid_data_list = [{'String-Ipv6': '2001:0db8:85a3:0000:0000:8a2e:0370:7334'},
        {'String-Ipv6': '2001:db8::'},
        {'String-Ipv6': 42540766411282592856903984951653826560}]
    invalid_data_list = [{'String-Ipv6': 'zzzz2001:db8:3333:4444:5555:6666:7777:8888zzzz'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_string_ipv4():
  
    j_schema = {
      "types": [
        ["String-Ipv4", "String", ["/ipv4"], ""]
      ]
    }
    
    valid_data_list = [{'String-Ipv4': '127.0.0.1'},
        {'String-Ipv4': 2130706433}]
    invalid_data_list = [{'String-Ipv4': 'zzzz127.0.0.1zzzz'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_string_idn_hostname():
  
    j_schema = {
      "types": [
        ["String-Idn-Hostname", "String", ["/idn-hostname"], ""]
      ]
    }
    
    valid_data_list = [{'String-Idn-Hostname': 'example.com'},
        {'String-Idn-Hostname': 'xn----gtbspbbmkef.xn--p1ai'}]
    invalid_data_list = [{'String-Idn-Hostname': 'qwerasdf'}]
    
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)          
    
def test_string_hostname():
  
    j_schema = {
      "types": [
        ["String-Hostname", "String", ["/hostname"], ""]
      ]
    }

    valid_data_list = [{'String-Hostname': 'example.com'},
        {'String-Hostname': '192.168.123.132'}]
    invalid_data_list = [{'String-Hostname': 'http://exam_ple.com'},
        {'String-Hostname': 'http://example.com'},
        {'String-Hostname': 'qwerasdf'}]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_idn_email():
  
    j_schema = {
      "types": [
        ["String-Idn-Email", "String", ["/idn-email"], ""]
      ]
    }

    valid_data_list = [{'String-Idn-Email': 'test@ツ.life'}]
    invalid_data_list = [{'String-Idn-Email': '@jarvis@stark.com'}]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_email():
  
    j_schema = {
      "types": [
        ["String-Email", "String", ["/email"], ""]
      ]
    }

    valid_data_list = [{'String-Email': 'jarvis@stark.com'},
        {'String-Email': 'jarvis@stark.eng.com'},
        {'String-Email': 'jarvis@stark-eng.com'},
        {'String-Email': '1jarvis@stark-eng.com'}]
    invalid_data_list = [{'String-Email': '@jarvis@stark.com'},
        {'String-Email': 'zzjarviszz'},
        {'String-Email': 'jarvis@stark-eng.com1'}]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_pattern():
  
    j_schema = {
      "types": [
        ["String-Pattern", "String", ["%^jarvis$"], ""]
      ]
    }

    valid_data_list = [{'String-Pattern': 'jarvis'}]
    invalid_data_list = [{'String-Pattern': 'JARVIS'},
        {'String-Pattern': 'zzjarviszz'}]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_time():
  
    j_schema = {
      "types": [
        ["String-Time", "String", ["/time"], ""]
      ]
    }

    now = datetime.datetime.now()
    current_time = now.time()

    valid_data_list = [{'String-Time': current_time}]
    invalid_data_list = [{'String-Time': 'hfdkjlajfdkl'},
        {'String-Time': 1596542285000}]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_date():
  
    j_schema = {
      "types": [
        ["String-Date", "String", ["/date"], ""]
      ]
    }

    valid_data_list = [{'String-Date': '2024-01-01'}]
    invalid_data_list = [{'String-Date': 'hfdkjlajfdkl'},
        {'String-Date': 'yy2024-01-01zz'},
        {'String-Date': datetime.datetime.now()},
        {'String-Date': 1596542285000}]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)
    assert err_count == 0
    
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_datetime():
  
    j_schema = {
      "types": [
        ["String-Datetime", "String", ["/date-time"], ""]
      ]
    }

    valid_data_list = [
            {'String-Datetime': '2024-01-01'},
            {'String-Datetime': datetime.datetime.now()},
            {'String-Datetime': 1596542285000}
        ]
    
    invalid_data_list = [
            {'String-Datetime': 'hfdkjlajfdkl'},
            {'String-Datetime': 'yy2024-01-01zz'}
        ]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
    
    err_count = validate_valid_data(custom_schema, invalid_data_list)    
    assert err_count == len(invalid_data_list)
  
def test_jadn_str():
  
    j_schema = {
      "types": [
        ["String-Type", "String", ["{4", "}12"], ""]
      ]
    }

    valid_data_list = [{'String-Type': 'test string'}]
    invalid_data_list = [
                    {'String-Type': 4323 },
                    {'String-Type': 'zz' },
                    {'String-Type': 'testing string' }
                ]
  
    custom_schema, err_count = create_testing_model(j_schema)
        
    err_count = validate_valid_data(custom_schema, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(custom_schema, invalid_data_list)
    assert err_count == len(invalid_data_list)