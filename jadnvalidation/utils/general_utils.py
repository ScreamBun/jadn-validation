import base64
import binascii
import datetime
import re
import sys
from typing import Any, Callable, Dict, Type, Union
from pydantic import BaseModel, create_model
from consts import ALLOWED_TYPE_OPTIONS
from jadnvalidation.models.jadn.info import Config

## From JADN Schema - START
def addKey(d: dict, k: str = None) -> Callable:
    """
    Decorator to append a function to a dict, referencing the function name or given key as the key in the dict
    :param d: dict to append the key/func onto
    :param k: key to use on the dict
    :return: original function
    """
    def wrapped(fun: Callable, key: str = k) -> Callable:
        d[key if key else fun.__name__] = fun
        return fun
    return wrapped

def check_values(val: Any) -> Any:
    """
    Check the value of the given arg and attempt to convert it to a bool, int, or float
    :param val: value to check
    :return: converted/original value
    """
    if isinstance(val, str):
        if val.lower() in ("true", "false"):
            return safe_cast(val, bool, val)

        if val.isdigit():
            return safe_cast(val, int, val)

        if re.match(r"^\d+\.\d+$", val):
            return safe_cast(val, float, val)

    return val

def default_decode(itm: Any, decoders: Dict[Type, Callable[[Any], Any]] = None) -> Any:
    """
    Default decode the given object to the predefined types
    :param itm: object to encode/decode,
    :param decoders: custom type decoding - Ex) -> {bytes: lambda b: b.decode('utf-8', 'backslashreplace')}
    :return: default system encoded object
    """
    if decoders and isinstance(itm, tuple(decoders.keys())):
        return decoders[type(itm)](itm)

    if isinstance(itm, dict):
        return {default_decode(k, decoders): default_decode(v, decoders) for k, v in itm.items()}

    if isinstance(itm, (list, set, tuple)):
        return type(itm)(default_decode(i, decoders) for i in itm)

    if isinstance(itm, (int, float)):
        return itm

    if isinstance(itm, str):
        return check_values(itm)

    return itm

def default_encode(itm: Any, encoders: Dict[Type, Callable[[Any], Any]] = None) -> Any:
    """
    Default encode the given object to the predefined types
    :param itm: object to encode/decode,
    :param encoders: custom type encoding - Ex) -> {bytes: lambda b: b.decode('utf-8', 'backslashreplace')}
    :return: default system encoded object
    """
    if encoders and isinstance(itm, tuple(encoders.keys())):
        return encoders[type(itm)](itm)

    if isinstance(itm, dict):
        return {default_encode(k, encoders): default_encode(v, encoders) for k, v in itm.items()}

    if isinstance(itm, (list, set, tuple)):
        return type(itm)(default_encode(i, encoders) for i in itm)

    if isinstance(itm, (int, float)):
        return itm

    return toStr(itm)


def ellipsis_str(val: str, cut: int = 100) -> str:
    """
    Terminate a string larger than 'cut' characters and append an ellipsis
    :param val: string to limit the size of
    :param cut: number of characters to terminate string at
    :return: original string or ellipsis string
    """
    if len(val) > cut:
        return f"{val[:cut]}..."
    return val


def floatString(num: Union[float, str]) -> Union[float, str]:
    """
    Convert the value between a float and prefixed string; float -> string, string -> float
    :param num: value to concert
    :return: converted value if available
    """
    prefix = "§£"
    if isinstance(num, float):
        return f"{prefix}{num}"

    if isinstance(num, str) and num.startswith(prefix) and num[1:].replace(".", "", 1).isdigit():
        return float(num[1:])

    return num


def isBase64(sb: Union[bytes, str]) -> bool:
    """
    Determine if the given value is a base64
    :param sb: value to check
    :return: bool if base64
    """
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except (binascii.Error, ValueError):
        return False


def safe_cast(val: Any, to_type: Type, default: Any = None) -> Any:
    """
    Cast the given value to the given type safely without an exception being thrown
    :param val: value to cast
    :param to_type: type to cast as
    :param default: default value if casting fails
    :return: cast value or given default/None
    """
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def toStr(s: Any) -> str:
    """
    Convert the given type to a default string
    :param s: item to convert to a string
    :return: converted string
    """
    return s.decode(sys.getdefaultencoding(), 'backslashreplace') if hasattr(s, 'decode') else str(s)


def unixTimeMillis(dt: datetime) -> float:
    """
    Convert the datetime to a unix timestamp
    :param dt: datetime to concert
    :return: unix timestamp
    """
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def get_max_len(cls) -> int:
    config = Config()
    if cls.__options__.maxv is None:
        try:
            maxProps = cls.__config__.info.get('$MaxString')
            
            if maxProps is None:
                maxProps = config.MaxElements              
            
        except AttributeError:
            maxProps = config.MaxElements
            pass   
    else:
        maxProps = cls.__options__.maxv or config.MaxElements
        
    return int(maxProps)


def get_max_len_binary(cls) -> int:
    config = Config()
    if cls.__options__.maxv is None:
        try:
            maxProps = cls.__config__.info.get('$MaxBinary')
            
            if maxProps is None:
                maxProps = config.MaxElements            
            
        except AttributeError:
            maxProps = config.MaxElements
            pass   
    else:
        maxProps = cls.__options__.maxv or config.MaxElements
        
    return int(maxProps)


def get_max_v(cls) -> int:
    config = Config()
    if cls.__options__.maxv is None:
        try:
            maxProps = cls.__config__.info.get('$MaxElements')
            
            if maxProps is None:
                maxProps = config.MaxElements        
            
        except AttributeError:
            maxProps = config.MaxElements
            pass
    else:
        maxProps = cls.__options__.maxv or config.MaxElements
        
    return int(maxProps)

## From JADN Schema - END


def create_dynamic_model(model_name: str, fields: dict) -> type[BaseModel]:
    return create_model(
        model_name,
        **fields
    )

def convert_binary_to_hex(binary_string):
    """Converts a binary string to its hexadecimal representation."""

    return hex(int(binary_string, 2))[2:]  # [2:] removes the '0x' prefix

def convert_list_to_dict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict

def get_jadn_type_opts(jadn_type_name: str) -> tuple:
    return ALLOWED_TYPE_OPTIONS.get(jadn_type_name)

def is_type(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], str):
            return True
    return False

def is_field(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], int):
            return True
    return False

def safe_get(lst, index, default=None):
    """Safely get an item from a list at a given index.

    Args:
        lst: The list to access.
        index: The index to retrieve.
        default: The value to return if the index is out of range.

    Returns:
        The item at the given index, or the default value if the index is out of range.
    """
    try:
        return lst[index]
    except IndexError:
        return default

def split_on_first_char(string):
    """Splits a string on the first character."""

    if not string:
        return []

    return [string[0], string[1:]]

def split_on_second_char(string):
    """Splits a string on the second character."""

    if not string:
        return []

    return [string[:2], string[2:]]
