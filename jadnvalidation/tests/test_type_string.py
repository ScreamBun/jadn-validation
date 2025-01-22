import datetime
from pydantic import ValidationError

from jadnvalidation.pydantic_schema import create_pyd_model


def test_string_regex():
  
    jadn_schema = {
      "types": [
        ["String-Regex", "String", ["/regex"], ""]
      ]
    }
    
    valid_data_1 = {'String-Regex': '.*ABA.?'}
    valid_data_2 = {'String-Regex': 'A(BB){1,4}'}
    invalid_data_1 = {'String-Regex': '['}
    invalid_data_2 = {'String-Regex': '\\'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                     
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)            
        
    assert error_count == 2

def test_string_relative_json_pointer():
  
    jadn_schema = {
      "types": [
        ["String-Relative-Json-Pointer", "String", ["/relative-json-pointer"], ""]
      ]
    }
    
    valid_data_1 = {'String-Relative-Json-Pointer': '0/foo'}
    valid_data_2 = {'String-Relative-Json-Pointer': '1/sin-city'}
    invalid_data_1 = {'String-Relative-Json-Pointer': '/foo/0'}
    invalid_data_2 = {'String-Relative-Json-Pointer': '-1/sin-city'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                     
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)            
        
    assert error_count == 2

def test_string_json_pointer():
  
    jadn_schema = {
      "types": [
        ["String-Json-Pointer", "String", ["/json-pointer"], ""]
      ]
    }
    
    valid_data_1 = {'String-Json-Pointer': '/foo'}
    valid_data_2 = {'String-Json-Pointer': '/foo/0'}
    invalid_data_1 = {'String-Json-Pointer': 'zzzz'}
    invalid_data_2 = {'String-Json-Pointer': ':///items.starfox'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                  
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)            
        
    assert error_count == 2

def test_string_iri_ref():
  
    jadn_schema = {
      "types": [
        ["String-Iri-Reference", "String", ["/iri-reference"], ""]
      ]
    }
    
    valid_data_1 = {'String-Iri-Reference': 'mailto:info@example.com'}
    valid_data_2 = {'String-Iri-Reference': 'file://localhost/absolute/path/to/file'}
    valid_data_3 = {'String-Iri-Reference': 'https://www.example.珠宝/'}
    invalid_data_1 = {'String-Iri-Reference': 'zzzz'}
    invalid_data_2 = {'String-Iri-Reference': ':///items.starfox'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    try:
        pyd_model.model_validate(valid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                  
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)            
        
    assert error_count == 2

def test_string_iri():
  
    jadn_schema = {
      "types": [
        ["String-Iri", "String", ["/iri"], ""]
      ]
    }
    
    valid_data_1 = {'String-Iri': 'http://puny£code.com'}
    valid_data_2 = {'String-Iri': 'https://www.аррӏе.com/'}
    valid_data_3 = {'String-Iri': 'https://www.example.珠宝/'}
    invalid_data_1 = {'String-Iri': 'zzzz'}
    invalid_data_2 = {'String-Iri': ':///items.starfox'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)              
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    try:
        pyd_model.model_validate(valid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                  
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)            
        
    assert error_count == 2

def test_string_uri_template():
  
    jadn_schema = {
      "types": [
        ["String-Uri-Template", "String", ["/uri-template"], ""]
      ]
    }
    
    valid_data_1 = {'String-Uri-Template': 'https://www.example.com/api/v1/items/{/item_id}'}
    invalid_data_1 = {'String-Uri-Template': 'zzzz'}
    invalid_data_2 = {'String-Uri-Template': '/items/{}'}
    invalid_data_3 = {'String-Uri-Template': 'https://www.example.com/api/v1/items/'}
    
    error_count = 0
    try :
        pyd_model = create_pyd_model(jadn_schema)    
        print(pyd_model)
    except Exception as err:
        print(err)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                 
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                    
        
    assert error_count == 3

def test_string_uri_ref():
  
    jadn_schema = {
      "types": [
        ["String-Uri-Ref", "String", ["/uri-reference"], ""]
      ]
    }
    
    valid_data_1 = {'String-Uri-Ref': 'http://www.example.com/questions/3456/my-document'}
    valid_data_2 = {'String-Uri-Ref': 'mailto:info@example.com'}
    valid_data_3 = {'String-Uri-Ref': 'file://localhost/absolute/path/to/file'}
    invalid_data_1 = {'String-Uri-Ref': 'zzzz'}
    invalid_data_2 = {'String-Uri-Ref': '//./file_at_current_dir'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(valid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(valid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(valid_data_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                     
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(invalid_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(invalid_data_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)            
        
    assert error_count == 2

def test_string_uri():
  
    jadn_schema = {
      "types": [
        ["String-Uri", "String", ["/uri"], ""]
      ]
    }
    
    string_uri_1 = {'String-Uri': 'http://www.example.com/questions/3456/my-document'}
    string_uri_2 = {'String-Uri': 'mailto:info@example.com'}
    string_uri_3 = {'String-Uri': 'foo://example.com:8042/over/there?name=ferret#nose'}
    string_uri_invalid_1 = {'String-Uri': 'zzzz'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:    
        pyd_model.model_validate(string_uri_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_uri_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_uri_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                 
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(string_uri_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1 

def test_string_ipv6():
  
    jadn_schema = {
      "types": [
        ["String-Ipv6", "String", ["/ipv6"], ""]
      ]
    }
    
    string_ipv6_1 = {'String-Ipv6': '2001:0db8:85a3:0000:0000:8a2e:0370:7334'}
    string_ipv6_2 = {'String-Ipv6': '2001:db8::'}
    string_ipv6_3 = {'String-Ipv6': 42540766411282592856903984951653826560}
    string_ipv6_invalid_1 = {'String-Ipv6': 'zzzz2001:db8:3333:4444:5555:6666:7777:8888zzzz'}
    
    error_count = 0
    try:
        pyd_model = create_pyd_model(jadn_schema)    
        print(pyd_model)
    except Exception as e:
        error_count = error_count + 1
        print(e)    
    
    try:
        pyd_model.model_validate(string_ipv6_1)       
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_ipv6_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_ipv6_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)               
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(string_ipv6_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1   

def test_string_ipv4():
  
    jadn_schema = {
      "types": [
        ["String-Ipv4", "String", ["/ipv4"], ""]
      ]
    }
    
    string_ipv4_1 = {'String-Ipv4': '127.0.0.1'}
    string_ipv4_2 = {'String-Ipv4': 2130706433}
    string_ipv4_invalid_1 = {'String-Ipv4': 'zzzz127.0.0.1zzzz'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(string_ipv4_1)       
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_ipv4_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(string_ipv4_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1   

def test_string_idn_hostname():
  
    jadn_schema = {
      "types": [
        ["String-Idn-Hostname", "String", ["/idn-hostname"], ""]
      ]
    }
    
    string_idn_hostname_1 = {'String-Idn-Hostname': 'example.com'}
    string_idn_hostname_2 = {'String-Idn-Hostname': 'xn----gtbspbbmkef.xn--p1ai'}
    string_idn_hostname_invalid_1 = {'String-Idn-Hostname': 'qwerasdf'}
    
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(string_idn_hostname_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_idn_hostname_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(string_idn_hostname_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 1           
    
def test_string_hostname():
  
    jadn_schema = {
      "types": [
        ["String-Hostname", "String", ["/hostname"], ""]
      ]
    }

    string_hostname_1 = {'String-Hostname': 'example.com'}
    string_hostname_2 = {'String-Hostname': '192.168.123.132'}
    string_hostname_invalid_1 = {'String-Hostname': 'http://exam_ple.com'}
    string_hostname_invalid_2 = {'String-Hostname': 'http://example.com'}
    string_hostname_invalid_3 = {'String-Hostname': 'qwerasdf'}
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(string_hostname_1)       
    except ValidationError as e:
        error_count = error_count + 1
        print(e)   
    
    try:
        pyd_model.model_validate(string_hostname_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)   
        
    assert error_count == 0         
    
    try:
        pyd_model.model_validate(string_hostname_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_hostname_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                                   
        
    try:
        pyd_model.model_validate(string_hostname_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                    
        
    assert error_count == 3

def test_string_idn_email():
  
    jadn_schema = {
      "types": [
        ["String-Idn-Email", "String", ["/idn-email"], ""]
      ]
    }

    string_idn_email_1 = {'String-Idn-Email': 'test@ツ.life'}
    string_idn_email_invalid_1 = {'String-Idn-Email': '@jarvis@stark.com'}
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(string_idn_email_1)        
    except ValidationError as e:
        error_count = error_count + 1
        print(e)   
        
    assert error_count == 0                           
        
    try:
        pyd_model.model_validate(string_idn_email_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                    
        
    assert error_count == 1

def test_string_email():
  
    jadn_schema = {
      "types": [
        ["String-Email", "String", ["/email"], ""]
      ]
    }

    string_pattern_email_1 = {'String-Email': 'jarvis@stark.com'}
    string_pattern_email_2 = {'String-Email': 'jarvis@stark.eng.com'}
    string_pattern_email_3 = {'String-Email': 'jarvis@stark-eng.com'}
    string_pattern_email_4 = {'String-Email': '1jarvis@stark-eng.com'}
    string_pattern_email_invalid_1 = {'String-Email': '@jarvis@stark.com'}
    string_pattern_email_invalid_2 = {'String-Email': 'zzjarviszz'}  
    string_pattern_email_invalid_3 = {'String-Email': 'jarvis@stark-eng.com1'}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(string_pattern_email_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)   
    
    try:
        pyd_model.model_validate(string_pattern_email_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_pattern_email_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_pattern_email_4)
    except ValidationError as e:
        error_count = error_count + 1
        print(e) 
        
    assert error_count == 0                           
        
    try:
        pyd_model.model_validate(string_pattern_email_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_pattern_email_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_pattern_email_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                      
        
    assert error_count == 3

def test_string_pattern():
  
    jadn_schema = {
      "types": [
        ["String-Pattern", "String", ["%^jarvis$"], ""]
      ]
    }

    string_pattern_data_1 = {'String-Pattern': 'jarvis'}
    string_pattern_data_invalid_1 = {'String-Pattern': 'JARVIS'}
    string_pattern_data_invalid_2 = {'String-Pattern': 'zzjarviszz'}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
    
    try:
        pyd_model.model_validate(string_pattern_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    assert error_count == 0  
    
    try:
        pyd_model.model_validate(string_pattern_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_pattern_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 2
    
def test_string_time():
  
    jadn_schema = {
      "types": [
        ["String-Time", "String", ["/time"], ""]
      ]
    }

    now = datetime.datetime.now()
    current_time = now.time()

    string_date_time_1 = {'String-Time': current_time}
    string_date_time_invalid_1 = {'String-Time': 'hfdkjlajfdkl'}
    string_date_time_invalid_2 = {'String-Time': 1596542285000}
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(string_date_time_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    assert error_count == 0
    
    try:
        pyd_model.model_validate(string_date_time_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_date_time_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)             
        
    assert error_count == 2
    
def test_string_date():
  
    jadn_schema = {
      "types": [
        ["String-Date", "String", ["/date"], ""]
      ]
    }

    string_date_data_1 = {'String-Date': '2024-01-01'}
    string_date_data_invalid_1 = {'String-Date': 'hfdkjlajfdkl'}
    string_date_data_invalid_2 = {'String-Date': 'yy2024-01-01zz'}  
    string_date_data_invalid_3 = {'String-Date': datetime.datetime.now()}
    string_date_data_invalid_4 = {'String-Date': 1596542285000}
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:       
        pyd_model.model_validate(string_date_data_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    assert error_count == 0
    
    try:
        pyd_model.model_validate(string_date_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_date_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_date_data_invalid_3)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_date_data_invalid_4)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)                
        
    assert error_count == 4
    
def test_string_datetime():
  
    jadn_schema = {
      "types": [
        ["String-Datetime", "String", ["/date-time"], ""]
      ]
    }

    string_datatime_data_1 = {'String-Datetime': '2024-01-01'}
    string_datatime_data_2 = {'String-Datetime': datetime.datetime.now()}
    string_datatime_data_3 = {'String-Datetime': 1596542285000}
    string_datatime_data_invalid_1 = {'String-Datetime': 'hfdkjlajfdkl'}
    string_datatime_data_invalid_2 = {'String-Datetime': 'yy2024-01-01zz'}  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(string_datatime_data_1)   
        pyd_model.model_validate(string_datatime_data_2)
        pyd_model.model_validate(string_datatime_data_3)        
    except ValidationError as e:
        error_count = error_count + 1
        print(e)       
        
    except ValidationError as e:
        error_count = error_count + 1
        print(e)  
        
    assert error_count == 0
    
    try:
        pyd_model.model_validate(string_datatime_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_datatime_data_invalid_2)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    assert error_count == 2
  
def test_jadn_str():
  
    jadn_schema = {
      "types": [
        ["String-Type", "String", ["{4", "}12"], ""]
      ]
    }

    string_data = {'String-Type': 'test string'}
    string_data_invalid_1 = {'String-Type': 4323 }
    string_data_invalid_2 = {'String-Type': 'zz' }
    string_data_invalid_3 = {'String-Type': 'testing string' }  
  
    error_count = 0
    pyd_model = create_pyd_model(jadn_schema)    
    print(pyd_model)
        
    try:
        pyd_model.model_validate(string_data)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 0        
        
    try:
        pyd_model.model_validate(string_data_invalid_1)
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_data_invalid_2)      
    except ValidationError as e:
        error_count = error_count + 1
        print(e)
        
    try:
        pyd_model.model_validate(string_data_invalid_3)      
    except ValidationError as e:
        error_count = error_count + 1
        print(e)        
        
    assert error_count == 3