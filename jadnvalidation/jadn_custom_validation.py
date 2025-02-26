from jadnvalidation.models.jadn.jadn_type import Base_Type, build_jadn_type_obj


def get_types(j_types: list, base_type: str):
    return [j_type for j_type in j_types if j_type[1] == base_type]

def arrary_validation(j_schema: dict, data: dict):
    """
    Custom validation for jadn arrays. 
    """
    j_types = j_schema.get('types')
    arrays = get_types(j_types, Base_Type.ARRAY.value)
    for array in arrays:
        j_type_obj = build_jadn_type_obj(array, {})
        test = ""
    
def custom_validation(j_schema: dict, data: dict):
    """
    Custom validations needed to cover pydantic limitations. 
    For instance, jadn array validation.  
    """
    
    # TODO: check if schema contains and array and if data contains the array name. 
    arrary_validation(j_schema, data)
    test = ""
    
    