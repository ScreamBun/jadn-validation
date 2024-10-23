from pydantic import ValidationError
from jadn import Info


def test_package():
    
    err_count = 0
    try:
        Info(package='http://www.example.com')
    except ValidationError as e:
        err_count = err_count + 1
        print(e)    
    
    # Negative test    
    try:
        Info(package='ftp://invalid.url')
    except ValidationError as e:
        err_count = err_count + 1
        print(e)
        
    # Negative test        
    try:
        Info(package='not a url')
    except ValidationError as e:
        err_count = err_count + 1
        print(e)
        
    try:
        Info(package='http://www.example.com', version='1.1.1', title='test title', description='test description', comment='test comment', license='test license')
    except ValidationError as e:
        err_count = err_count + 1
        print(e)
    
    # Negative test    
    try:
        Info(package='http://www.example.com', version=1, title='test title', description='test description', comment='test comment', license='test license')
    except ValidationError as e:
        err_count = err_count + 1
        print(e)    
        
    try:
        Info(package='http://www.example.com', namespaces={'test1': 'test1', 'test2': 'test2'})
    except ValidationError as e:
        err_count = err_count + 1
        print(e)
        
    # Negative test
    try:
        Info(package='http://www.example.com', namespaces='test1')
    except ValidationError as e:
        err_count = err_count + 1
        print(e)                               
        
    assert int(err_count) == 4