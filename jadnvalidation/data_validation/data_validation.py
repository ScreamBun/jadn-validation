from jadnvalidation.utils.general_utils import create_clz_instance, get_schema_type_by_name


class DataValidation:
    j_schema: dict = {}
    root: str = None
    data: dict = {}
    
    def __init__(self, j_schema: dict, root: str, data: dict):
        self.j_schema = j_schema
        self.root = root
        self.data = data
        
    def validate(self):
        
        try:
            j_types = self.j_schema.get('types')
            root_type = get_schema_type_by_name(j_types, self.root)[0]   
            # root_name = root_type[0]
            root_base_type = root_type[1]
            # root_data = get_data_by_name(self.data, root_name)
            
            clz_instance = create_clz_instance(root_base_type, self.j_schema, root_type, self.data)
            clz_instance.validate()            
            
        except Exception as err:           
            raise ValueError(err)