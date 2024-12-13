import re
from urllib.parse import urlparse
import jsonpointer

from typing import Union

from jadnvalidation.utils.general_utils import addKey


GeneralFormats = {}


# Use regex from https://stackoverflow.com/questions/201323/how-to-validate-an-email-address-using-a-regular-expression
#   A more comprehensive email address validator is available at http://isemail.info/about
@addKey(d=GeneralFormats)
def email(val: str) -> str:
    """
    Check if valid E-Mail address - RFC 5322 Section 3.4.1
    :param val: E-Mail address to validate
    :return: given e-mail
    :raises: TypeError, ValueError
    """
    if not isinstance(val, str):
        raise TypeError(f"E-Mail given is not expected string, given {type(val)}")
    rfc5322_re = (
        r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
        r'"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@'
        r"(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])"
        r"|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]"
        r":(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    )
    if not re.match(rfc5322_re, val):
        raise ValueError("E-Mail given is not valid")
    return val


@addKey(d=GeneralFormats)
def uri(val: str) -> str:
    """
    Check if valid URI - RFC 3986
    :param val: URI to validate
    :return: uri given
    :raises TypeError, ValueError
    """
    if not isinstance(val, str):
        raise TypeError(f"URI given is not expected string, given {type(val)}")
    url_match = re.match(r"(https?:\/\/(www\.)?)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", val)

    result = urlparse(val)
    if not all([result.scheme, result.netloc, result.path]) or url_match:
        raise ValueError("URI given is not expected valid")
    return val


@addKey(d=GeneralFormats, k="json-pointer")
def json_pointer(val: str) -> jsonpointer.JsonPointer:
    """
    Validate JSON Pointer - RFC 6901 Section 5
    :param val: JSON Pointer to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"JSON Pointer given is not expected string, given {type(val)}")
    return jsonpointer.JsonPointer(val)


# Definition taken from: https://tools.ietf.org/html/draft-handrews-relative-json-pointer-01#section-3
@addKey(d=GeneralFormats, k="relative-json-pointer")
def relative_json_pointer(val: str) -> jsonpointer.JsonPointer:
    """
    Validate Relative JSON Pointer - JSONP
    :param val: Relative JSON Pointer to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"relative json pointer given is not expected string, given {type(val)}")

    non_negative_integer, rest = [], ""
    for i, character in enumerate(val):
        if character.isdigit():
            non_negative_integer.append(character)
            continue
        if not non_negative_integer:
            raise ValueError("invalid relative json pointer given")
        rest = val[i:]
        break
    try:
        (rest == "#") or jsonpointer.JsonPointer(rest)
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err
    return json_pointer.JsonPointer(val)


@addKey(d=GeneralFormats)
def regex(val: str) -> re.Pattern:
    """
    Validate Regular Expression - ECMA 262
    :param val: RegEx to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"RegEx given is not expected string, given {type(val)}")

    return re.compile(val)


@addKey(d=GeneralFormats, k="i8")
def bit_8(val: int) -> int:
    """
    Validate 8-bit number - Signed 8-bit integer, value must be between -128 and 127
    :param val: number to validate
    :return: None or Exception
    """
    if not isinstance(val, int):
        raise TypeError(f"number given is not expected integer, given {type(val)}")

    if len(f"{abs(val):b}") > 8:
        raise ValueError(f"number is not 8-bit, {val}")
    return val


@addKey(d=GeneralFormats, k="i16")
def bit_16(val: int) -> int:
    """
    Validate 16-bit number - Signed 16-bit integer, value must be between -32768 and 62767
    :param val: number to validate
    :return: None or Exception
    """
    if not isinstance(val, int):
        raise TypeError(f"number given is not expected integer, given {type(val)}")

    if len(f"{abs(val):b}") > 16:
        raise ValueError(f"number is not 16-bit, {val}")
    return val


@addKey(d=GeneralFormats, k="i32")
def bit_32(val: int) -> int:
    """
    Validate 36-bit number - Signed 36-bit integer, value must be between -2147483648 and 2147483647
    :param val: number to validate
    :return: None or Exception
    """
    if not isinstance(val, int):
        raise TypeError(f"number given is not expected integer, given {type(val)}")

    if len(f"{abs(val):b}") > 32:
        raise ValueError(f"number is not 32-bit, {val}")
    return val


@addKey(d=GeneralFormats, k="unsigned")
def unsigned(n: int, val: Union[bytes, int]) -> Union[bytes, int]:
    """
    Validate an Unsigned integer or bit field of <n> bits, value must be between 0 and 2^<n> - 1
    :param n: max value of the integer/bytes - 2^<n> - 1
    :param val: integer/bytes to validate
    :return: None or Exception
    """
    if not isinstance(val, (bytes, int, str)):
        raise TypeError(f"unsigned bytes/number given is not expected bytes/integer, given {type(val)}")

    # Maximum bytes/number
    max_val = pow(2, n) - 1

    # Unsigned Integer
    if isinstance(val, int):
        msg = "cannot be negative" if val < 0 else (f"cannot be greater than {max_val:,}" if val > max_val else None)
        raise ValueError(f"unsigned integer given is invalid, {msg}") if msg else None

    # Unsigned Bytes
    val = bytes(val, "utf-8") if isinstance(val, str) else val
    if val and len(val) > max_val:
        raise ValueError(f"unsigned bytes given is invalid, cannot be more than {max_val:,} bytes")
    return val
