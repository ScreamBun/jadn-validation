from typing import Union

from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, is_primitive
from jadnvalidation.utils.general_utils import create_clz_instance, get_reference_type
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_vtype, is_optional

rules = {
    "type": "check_type",
    "fields": "check_vtype",
    "{": "check_minv",
    "}": "check_maxv"
}

class ArrayOf:
    
    j_schema: dict = {}
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The array of's data only
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data  
        
    def check_type(self):
        if not isinstance(self.data, list):
            # Note: If the data isn't a list, there's no point to continue with other checks
            # Just raise the error to kill the thread rather than collecting and continuing. 
            raise ValueError(f"Data must be a list. Received: {type(self.data)}")
        
    def check_minv(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Array length must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_maxv(self):
        max_length = get_max_length(self.j_type)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Array length must be less than {max_length}. Received: {len(self.data)}")
        
    def check_vtype(self):
        vtype = get_vtype(self.j_type)
        
        if self.data is None:
            if not is_optional(self.j_type):
                self.errors.append(f"Array '{self.j_type.type_name}' missing data")        
        
        for data_item in self.data:
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