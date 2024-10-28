from typing import Annotated
from pydantic import StringConstraints


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

# regex
REGEX_EMAIL = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# custom pyd types
DomainName = Annotated[str, StringConstraints(pattern=r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")]