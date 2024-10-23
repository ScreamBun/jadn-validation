from typing import Any, Dict, Optional
from pydantic import BaseModel


class Jadn_Parent(BaseModel):
    
    # Source: https://github.com/pydantic/pydantic/issues/1937#issuecomment-695313040
    @classmethod
    def add_fields(cls, **field_definitions: Any):
        new_fields: Dict[str, FieldInfo] = {}
        new_annotations: Dict[str, Optional[type]] = {}

        for f_name, f_def in field_definitions.items():
            if isinstance(f_def, tuple):
                try:
                    f_annotation, f_value = f_def
                except ValueError as e:
                    raise Exception(
                        'field definitions should either be a tuple of (<type>, <default>) or just a '
                        'default value, unfortunately this means tuples as '
                        'default values are not allowed'
                    ) from e
            else:
                f_annotation, f_value = None, f_def

            if f_annotation:
                new_annotations[f_name] = f_annotation

            new_fields[f_name] = FieldInfo(annotation=f_annotation)

        cls.model_fields.update(new_fields)
        cls.model_rebuild(force=True)    