from typing import Literal
from pydantic import BaseModel

from jadnvalidation.pydantic_schema import create_pyd_model, pyd_data_validation


def create_testing_model(j_schema: dict) -> tuple[type[BaseModel] | dict, Literal[0, 1]]:
    err_count = 0
    custom_schema = {}
    try :
        custom_schema = create_pyd_model(j_schema)
    except Exception as err:
        err_count = err_count + 1
        print(err)
    return custom_schema, err_count

def validate_valid_data(schema: type[BaseModel], data_list: list) -> int:
    err_count = 0
    for data in data_list:
        try :
            pyd_data_validation(schema, data)
        except Exception as err:
            err_count = err_count + 1
            print(err)
    return err_count

def validate_invalid_data(schema: type[BaseModel], data_list: list) -> int:
    err_count = 0
    for data in data_list:
        try :
            pyd_data_validation(schema, data)
        except Exception as err:
            err_count = err_count + 1
            print(err)
    return err_count