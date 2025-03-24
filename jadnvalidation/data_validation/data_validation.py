from typing import Union
from jadnvalidation.utils.general_utils import create_clz_instance, get_schema_type_by_name


class DataValidation:
    j_schema: dict = {}
    root: Union[str, list] = None
    data: dict = {}
    
    def __init__(self, j_schema: dict, root: Union[str, list], data: dict):
        self.j_schema = j_schema
        self.root = root
        self.data = data
        
    def validate(self):
        
        try:
            j_types = self.j_schema.get('types')
            if j_types == None or j_types == []:
                raise ValueError(f"No Types defined")
                       
            # TODO: Loop for multiple roots
            roots: list = []
            if isinstance(self.root, str):
                roots.append(self.root)
            elif isinstance(self.root, list):
                roots = self.root
            else:
                raise ValueError(f"Invalid Root Type")           
            
            for root_item in roots:
                root_type = get_schema_type_by_name(j_types, root_item)
                if root_type == None:
                    raise ValueError(f"Root Type not found {root_item}")
                
                clz_instance = create_clz_instance(root_type[1], self.j_schema, root_type, self.data)
                clz_instance.validate()            
            
        except Exception as err:           
            raise ValueError(err)