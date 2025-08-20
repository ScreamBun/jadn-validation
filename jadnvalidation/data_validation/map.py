from typing import Union

from build.lib.jadnvalidation.models.jadn.jadn_config import check_type_name
from jadnvalidation.models.jadn.jadn_type import build_jadn_type_obj, is_field_multiplicity
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_field_name, check_sys_char, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, is_user_defined
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance, get_data_by_id, get_data_by_name, merge_opts
from jadnvalidation.utils.mapping_utils import flip_to_array_of, get_max_length, get_max_occurs, get_min_length, get_min_occurs, get_tagged_data, is_optional, use_field_ids
from jadnvalidation.utils.type_utils import get_reference_type

common_rules = {
    "type": "check_type",
    "{": "check_min_length",
    "}": "check_max_length",
    "fields": "check_fields",
    "extra_fields": "check_extra_fields"
}

json_rules = {}
xml_rules = {}

class Map:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The map data only
    data_format: str = None
    use_ids: bool = False
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format         
        
        self.use_ids = use_field_ids(self.j_type.type_options)
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_type(self):
        if not isinstance(self.data, dict):
            raise ValueError(f"Data must be a map / dict. Received: {type(self.data)}")
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")
        
    def check_fields(self):
        for j_key, j_field in enumerate(self.j_type.fields):
            j_field_obj = build_jadn_type_obj(j_field)
            
            field_data = None
            if self.use_ids:
                field_data = get_data_by_id(self.data, j_field_obj.id)
            else:
                field_data = get_data_by_name(self.data, j_field_obj.type_name)                
            
            if field_data is None:
                if is_optional(j_field_obj):
                    continue
                else:
                    raise ValueError(f"Field '{j_field_obj.type_name}' is missing from data")
                
            check_sys_char(j_field_obj.type_name, self.j_config.Sys)
            check_field_name(j_field_obj.type_name, self.j_config.FieldName)                

            if is_field_multiplicity(j_field_obj.type_options):
                j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))

            elif is_user_defined(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                j_field_obj = ref_type_obj
                j_field_obj.type_options = merged_opts
                
            tagged_data = get_tagged_data(j_field_obj, self.data)
                
            clz_kwargs = dict(
                class_name=j_field_obj.base_type,
                j_schema=self.j_schema,
                j_type=j_field_obj,
                data=field_data,
                data_format=self.data_format
            )
            if tagged_data is not None:
                clz_kwargs['tagged_data'] = tagged_data

            clz_instance = create_clz_instance(**clz_kwargs)
            clz_instance.validate()
            
    def check_extra_fields(self):
        # Check if data has any unknown fields
        if self.data is not None:
            
            if len(self.data) > len(self.j_type.fields):
                raise ValueError(f"Data has more fields ({len(self.data)}) than allowed ({len(self.j_type.fields)})")
            
            for data_key in self.data.keys():
                is_found = False
                for j_field in self.j_type.fields:
                    if self.use_ids:
                        if data_key == str(j_field[0]):
                            is_found = True
                    elif data_key == j_field[1]:
                        is_found = True
                        
                if not is_found:
                    raise ValueError(f"Data field '{data_key}' is not defined in schema")
        
    def validate(self):
        
        # Check data against rules
        rules = json_rules
        if self.data_format == XML:
            rules = xml_rules
       
       # Data format specific rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
            
        # Common rules across all data formats
        for key, function_name in common_rules.items():
            getattr(self, function_name)()            
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True
