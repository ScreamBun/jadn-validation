from jadnvalidation.jadn_custom_validation import custom_validation
from jadnvalidation.pydantic_schema import create_pyd_model, pyd_data_validation


class JadnValidation:
    j_schema = {}
    data = {}
    errors = []
    
    def __init__(self, j_schema: dict, data: dict):
        self.j_schema = j_schema
        self.data = data
        
    def validate(self):
        # Create Pydantic model
        # p_model = create_pyd_model(self.j_schema)
        
        # Validate data using Pydantic model
        # try :
        #     pyd_data_validation(p_model, self.data)
        # except Exception as err: 
        #     self.errors.append(ValueError(err))
            
        # Validate data using custom validations
        try :
            custom_validation(self.j_schema, self.data)
        except Exception as err:
            self.errors.append(ValueError(err))
            
        # Raise exception if errors exist
        if len(self.errors) > 0:
            raise ValueError(self.errors)            