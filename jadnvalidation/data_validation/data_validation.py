from typing import Union

from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_type_name, get_j_config
from jadnvalidation.models.jadn.jadn_type import build_jadn_type_obj
from jadnvalidation.utils.consts import CBOR, JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance, get_err_msgs, get_schema_type_by_name
from jadnxml.builder.xml_builder import build_py_from_xml


class DataValidation:
    j_schema: dict = {}
    j_config: Jadn_Config = None
    root: Union[str, list] = None
    data: dict = {}
    data_format: str = None
    
    def __init__(self, j_schema: dict, root: Union[str, list], data: dict, data_format = JSON):
        self.j_schema = j_schema
        self.root = root
        self.data = data
        self.data_format = data_format
        self.j_config = get_j_config(self.j_schema)        
        
    def validate(self):
        
        try:
            
            if self.data_format == JSON:
                # TODO: Move str to json conversion here
                # self.data = 
                pass             
            
            elif self.data_format == XML:
                self.data = build_py_from_xml(self.j_schema, self.root, self.data)
                
            elif self.data_format == CBOR:
                # TODO: Move str to cbor conversion here
                # self.data = 
                pass
            else:
                raise ValueError(f"Invalid Data Format: {self.data_format}")
            
            j_types = self.j_schema.get('types')
            if j_types == None or j_types == []:
                raise ValueError(f"No Types defined")  
                    
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
                
                root_type_obj = build_jadn_type_obj(root_type)
                check_type_name(root_type_obj.type_name, self.j_config.TypeName)
                    
                clz_instance = create_clz_instance(root_type_obj.base_type, self.j_schema, root_type, self.data, self.data_format)
                clz_instance.validate()            
            
        except Exception as err:
            errs = get_err_msgs(err)       
            raise ValueError(errs)