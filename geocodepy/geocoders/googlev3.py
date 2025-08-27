import warnings

from geocodepy.geocoders.google import GoogleV3

__all__ = ("GoogleV3",)

warnings.warn(
    "`geocodepy.geocoders.googlev3` module is deprecated. "
    "Use `geocodepy.geocoders.google` instead. "
    "In geopy 3 this module will be removed.",
    DeprecationWarning,
    stacklevel=2,
)
