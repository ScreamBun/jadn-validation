
import rfc3986

from jadnvalidation.utils.general_utils import addKey

RFC3986_Formats = {}

@addKey(d=RFC3986_Formats, k="uri")
def uri(val: str) -> rfc3986.ParseResult:
    """
    Validate an URI - RFC 3987
    :param val: URI instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"uri given is not expected string, given {type(val)}")

    try:
        return rfc3986.urlparse(val)
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err


@addKey(d=RFC3986_Formats, k="uri-reference")
def uri_reference(val: str) -> rfc3986.URIReference:
    """
    Validate an URI-Reference - RFC 3987
    :param val: URI-Reference instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"uri-reference given is not expected string, given {type(val)}")

    try:
        return rfc3986.uri_reference(val)
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err
