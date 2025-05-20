from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance
from jadnvalidation.utils.mapping_utils import is_optional
        
        
common_rules = {
    "type": "check_type",
    "length": "check_length",
    "fields": "check_data"
}

json_rules = {}
xml_rules = {}        
        
class Ipv4Net:
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Jadn_Type = None
    data: any = None
    data_format: str = None    
    errors = []    
    
    def __init__(self, j_schema: dict = {}, j_type: Jadn_Type = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format          
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
                
    def build_j_type_ipv4_addr(self) -> Jadn_Type:
        jadn_type_obj = Jadn_Type(
                type_name="ipv4_addr", 
                base_type="Binary", 
                type_options=["/ipv4-addr", "{1", "[1"], 
                type_description="IPv4 address as defined in [[RFC0791]](#rfc0791)",
                fields=[])
        
        return jadn_type_obj
    
    def build_j_type_prefix_length(self) -> Jadn_Type:
        jadn_type_obj = Jadn_Type(
                type_name="prefix_length", 
                base_type="Integer", 
                type_options=["{0", "}32", "[0"], 
                type_description="CIDR prefix-length. If omitted, refers to a single host address.",
                fields=[])
        
        return jadn_type_obj              
                
    def check_type(self):
        if not isinstance(self.data, list):
            raise ValueError(f"Data for type {self.j_type.type_name} must be a list. Received: {type(self.data)}")                
           
    def check_length(self):
        if self.data is None:
            if not is_optional(self.j_type):
                raise ValueError(f"Missing required data for type {self.j_type.type_name}")
        else:            
            list_length = len(self.data)
            if list_length < 1: 
                raise ValueError(f"Data for type {self.j_type.type_name} must have at least 1 element (ipv4_addr). Received: {list_length}")
            
            if list_length > 2: 
                raise ValueError(f"Data for type {self.j_type.type_name} must be no larger than 2 elements (ipv4_addr & prefix length). Received: {list_length}")
        
    def check_data(self):
        j_type_ipv4_addr = self.build_j_type_ipv4_addr()
        j_type_prefix_length = self.build_j_type_prefix_length()
        
        for j_index, field_data in enumerate(self.data):  
                
            if j_index == 0:
                clz_instance = create_clz_instance(j_type_ipv4_addr.base_type, self.j_schema, j_type_ipv4_addr, field_data, self.data_format)
                clz_instance.validate()
                
            elif j_index == 1:
                
                if field_data is not None:
                    clz_instance = create_clz_instance(j_type_prefix_length.base_type, self.j_schema, j_type_prefix_length, field_data, self.data_format)
                    clz_instance.validate()      
    
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
