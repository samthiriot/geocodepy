import warnings

from geocodepy.geocoders.nominatim import Nominatim

__all__ = ("Nominatim",)

warnings.warn(
    "`geocodepy.geocoders.osm` module is deprecated. "
    "Use `geocodepy.geocoders.nominatim` instead. "
    "In geopy 3 this module will be removed.",
    DeprecationWarning,
    stacklevel=2,
)
