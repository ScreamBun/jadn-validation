from jadnvalidation.custom_validation.array import Array


def custom_validation(j_schema: dict, data: dict):
    """
    Custom validations needed to cover pydantic limitations. 
    For instance, jadn array validation.  
    """
    
    # TODO: check if schema contains and array and if data contains the array name. 
    av = Array(j_schema, data)
    av.validate()
    
    # TODO: Add more custom validations here...