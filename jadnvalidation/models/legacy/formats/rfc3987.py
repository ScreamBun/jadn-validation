import rfc3987

from typing import Any, Optional, TypedDict

from jadnvalidation.utils.general_utils import addKey


RFC3987_Formats = {}

class ParseResults(TypedDict):
    scheme: str
    authority: str
    # userinfo
    # host: str
    # port: int
    path: str
    query: Optional[Any]
    fragment: Optional[str]

@addKey(d=RFC3987_Formats, k="iri")
def iri(val: str) -> ParseResults:
    """
    Validate an IRI - RFC 3987
    :param val: IRI instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"iri given is not expected string, given {type(val)}")

    try:
        return ParseResults(**rfc3987.parse(val, rule="IRI"))
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err

@addKey(d=RFC3987_Formats, k="iri-reference")
def iri_reference(val: str) -> ParseResults:
    """
    Validate an IRI-Reference - RFC 3987
    :param val: IRI-Reference instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"iri given is not expected string, given {type(val)}")

    try:
        return ParseResults(**rfc3987.parse(val, rule="IRI_reference"))
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err
