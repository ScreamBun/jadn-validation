from typing import Union

from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_map_of_data_content, get_reference_type
from jadnvalidation.utils.mapping_utils import get_ktype, get_max_length, get_min_length, get_vtype, is_optional

# id, extend, minv, maxv
rules = {
    "type": "check_type",
    "{": "check_minv",
    "}": "check_maxv",
    "key_values": "check_key_values",
}

class MapOf:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The map of data only
    inner_data: any = None # The inner iterable data of the map
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data  
        
        if self.data:
            self.inner_data = get_map_of_data_content(self.data)
        
    def check_type(self):
        if self.inner_data:
            if not isinstance(self.inner_data, list):
                raise ValueError(f"Data must be a dict / object / record that contains an iterable structure. Received: {type(self.data)}")
        
    def check_minv(self):
        min_length = get_min_length(self.j_type.type_options)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_maxv(self):
        # TODO: Add in config max length check
        max_length = get_max_length(self.j_type.type_options)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")

    def check_keys(self):
        # for k, v in val.items():
        #     try:
        #         k_cls.validate(k) 
        #     except:
        #         raise ValueError(f"`{k}` is not a valid ktype`{ktype}`")     
        #     try:
        #         v_cls.validate(v)
        #     except:
        #         raise ValueError(f"`{v}` is not a valid vtype `{vtype}`")
        test = ""
        
    def check_key_values(self):
        vtype = get_vtype(self.j_type)
        ktype = get_ktype(self.j_type)
        
        if self.data is None:

            if not is_optional(self.j_type.type_options):
                self.errors.append(f"Map of '{self.j_type.type_name}' missing data")
        
        for data_item in self.inner_data:
            if is_primitive(vtype):
                of_jtype = Jadn_Type("of_" + self.j_type.type_name, vtype, self.j_type.config)
                clz_instance = create_clz_instance(vtype, self.j_schema, of_jtype, data_item)
                clz_instance.validate()
            else:                
                ref_type = get_reference_type(self.j_schema, vtype)
                ref_type_obj = build_j_type(ref_type, self.j_type.config)
                clz_instance = create_clz_instance(ref_type_obj.base_type, self.j_schema, ref_type_obj, data_item)
                clz_instance.validate()
        
    def validate(self):
        
        # Check data against rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
        
        # Other Checks.....?
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)
        
        return True
