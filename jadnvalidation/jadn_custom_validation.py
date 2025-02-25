def custom_validation(jadn_schema: dict, data: dict):
    """
    Custom validations needed to cover pydantic limitations. 
    For instance, jadn array validation.  
    """
    
    # TODO: check if schema contains and array and if data contains the array name. 
    test = ""
    
    