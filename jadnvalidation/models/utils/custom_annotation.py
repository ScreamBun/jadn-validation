from typing import Annotated

from pydantic import BeforeValidator, StringConstraints

from jadnvalidation.models.utils import general_utils


Hostname = Annotated[str, StringConstraints(pattern=r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")]
# Hostname = Annotated[str, BeforeValidator(general_utils.validate_domain)]
IdnHostname = Annotated[str, BeforeValidator(general_utils.validate_idn_domain)]
PydJsonPointer = Annotated[str, BeforeValidator(general_utils.validate_json_pointer)]
PydRelJsonPointer = Annotated[str, BeforeValidator(general_utils.validate_rel_json_pointer)]
PydRegex = Annotated[str, BeforeValidator(general_utils.validate_regex)]
BinaryHex = Annotated[str, BeforeValidator(general_utils.validate_hex)]