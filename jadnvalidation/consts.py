ALLOWED_TYPE_OPTIONS = {
    # Primitives
    "Binary" : ["{", "}", "/"], 
    "Boolean": [],
    "Integer": ["{", "}", "/"],
    "Number": ["y", "z", "/"], 
    "String": ["{", "}", "/", "%"],
    # Structures
    "Array": ["X", "/", "{", "}"],
    "ArrayOf": ["*", "{", "}", "q", "s", "b"],
    "Choice": ["=", "X"],
    "Enumerated": ["=", "#", ">", "X"],
    "Map": ["=", "X", "{", "}"],
    "MapOf": ["+", "*", "{", "}"],
    "Record": ["X", "{", "}"]
}

DYNAMIC_MODEL = "DynamicModel"