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
    
    def __init__(self):
        pass
    
    def validate_test(j_schema: dict, root: str, data_list: list) -> int:
        
        err_count = 0
        for data in data_list:
            try :
                j_validation = DataValidation(j_schema, root, data)
                j_validation.validate()
            except Exception as err:
                err_count = err_count + 1
                print(err)
        return err_count