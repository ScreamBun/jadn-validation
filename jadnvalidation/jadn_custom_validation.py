from jadnvalidation.custom_validation.array_validation import ArrayValidation


def custom_validation(j_schema: dict, data: dict):
    """
    Custom validations needed to cover pydantic limitations. 
    For instance, jadn array validation.  
    """
    
    # TODO: check if schema contains and array and if data contains the array name. 
    av = ArrayValidation(j_schema, data)
    av.validate()
    
    # TODO: Add more custom validations here...