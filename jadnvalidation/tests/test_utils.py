from jadnvalidation.data_validation.data_validation import DataValidation


def validate_valid_data(j_schema: dict, root: str, data_list: list) -> int:
    
    err_count = 0
    for data in data_list:
        try :
            j_validation = DataValidation(j_schema, root, data)
            j_validation.validate()
        except Exception as err:
            err_count = err_count + 1
            print(err)
    return err_count

def validate_invalid_data(j_schema: dict, root: str, data_list: list) -> int:
    
    err_count = 0
    for data in data_list:
        try :
            j_validation = DataValidation(j_schema, root, data)
            j_validation.validate()
        except Exception as err:
            err_count = err_count + 1
            print(err)
    return err_count

class Utils:
    
    j_schema: dict = None
    root: str = None
    tests: list = None
    
    def __init__(self, j_schema: dict = None, root: str = None, tests: list = None):
        self.j_schema = j_schema
        self.root = root
        self.tests = tests
    
    def validate_test(self) -> int:
        
        err_count = 0
        for test in self.tests:
            try :
                j_validation = DataValidation(self.j_schema, self.root, test)
                j_validation.validate()
            except Exception as err:
                err_count = err_count + 1
                print(err)
        return err_count