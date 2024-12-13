from jadnvalidation.models.pyd.formats.general import GeneralFormats
from jadnvalidation.models.pyd.formats.idna import IDNA_Formats
from jadnvalidation.models.pyd.formats.network import NetworkFormats
from jadnvalidation.models.pyd.formats.rfc3339 import RFC3339_Formats
from jadnvalidation.models.pyd.formats.rfc3986 import RFC3986_Formats
from jadnvalidation.models.pyd.formats.rfc3987 import RFC3987_Formats

ValidationFormats = {
    **GeneralFormats,
    **IDNA_Formats,
    **NetworkFormats,
    **RFC3339_Formats,
    **RFC3986_Formats,
    **RFC3987_Formats
}

__all__ = ["ValidationFormats"]