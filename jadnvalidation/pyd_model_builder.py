

from pydantic import create_model
from jadnvalidation.models.jadn.jadn_config import Jadn_Config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, is_primitive
from jadnvalidation.pydantic_schema import build_pyd_field


class PydModelBuilder:
    
    j_config_obj: Jadn_Config = Jadn_Config()
    errors = []
    
    def __init__(self):
        pass
        
    def build_model_from_j_type(self, j_type_obj: Jadn_Type):
        p_fields = {}
        pyd_model = None
        
        if is_primitive(j_type_obj):
            p_field = build_pyd_field(j_type_obj)
            p_fields[j_type_obj.type_name] = p_field
            pyd_model = create_model(j_type_obj.type_name, **p_fields)                
        else:
            raise ValueError("Unknown JADN Type")
        
        return pyd_model  
           
        
    def build_model_from_j_types(j_types: list):
        p_fields = {}