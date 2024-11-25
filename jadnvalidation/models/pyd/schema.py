from pydantic import BaseModel, Field


class Schema(BaseModel):
    # info: Optional[Information] = Field(default_factory=Information)
    types: dict = Field(default_factory=dict)  # Dict[str, Definition]
    # _info: bool = PrivateAttr(False)
    # __formats__: Dict[str, Callable] = ValidationFormats

    def __init__(self, **kwargs):
        # if "info" in kwargs and "namespaces" in kwargs["info"]:
        #     nms = set(kwargs["info"]["namespaces"])
        # else: 
        #     nms = None
        
        # if "info" in kwargs and "config" in kwargs["info"]:
        #     DefinitionBase.__config__.info = kwargs["info"]["config"]
        hit = ""
    
        if "types" in kwargs:
            # Create types... 
            hit = ""
            # kwargs["types"] = update_types(kwargs["types"], self.__formats__, nms)
            
        # super().__init__(**kwargs)
        # DefinitionBase.__config__.types = self.types