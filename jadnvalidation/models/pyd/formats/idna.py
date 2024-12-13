import email
import re

from jadnvalidation.models.pyd.formats.network import hostname
from jadnvalidation.utils.general_utils import addKey


IDNA_Formats = {}


@addKey(d=IDNA_Formats, k="idn-hostname")
def idn_hostname(val: str) -> str:
    """
    Validate an IDN Hostname - RFC 5890 § 2.3.2.3
    :param val: IDN Hostname to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"IDN Email given is not expected string, given {type(val)}")

    val = re.sub(r"^https?://", "", val)
    try:
        val = val.encode("idna")
    except Exception as err:
        raise ValueError from err
    val = val.decode("utf-8") if isinstance(val, bytes) else val
    return hostname(val)


@addKey(d=IDNA_Formats, k="idn-email")
def idn_email(val: str) -> str:
    """
    Validate an IDN Email - RFC 6531
    :param val: IDN Email to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"IDN Email given is not expected string, given {type(val)}")

    val = val.split("@")
    if len(val) != 2:
        raise ValueError("IDN Email address invalid")

    try:
        val = b"@".join([v.encode("idna") for v in val]).decode("utf-8")
    except Exception as err:
        print(f"{val} - {err}")
        raise ValueError from err
    return email(val)
