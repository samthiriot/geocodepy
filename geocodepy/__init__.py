"""
geopy is a Python client for several popular geocoding web services.

geopy makes it easy for Python developers to locate the coordinates of
addresses, cities, countries, and landmarks across the globe using third-party
geocoders and other data sources.

geopy is tested against CPython (versions 3.7, 3.8, 3.9, 3.10, 3.11, 3.12)
and PyPy3. geopy 1.x line also supported CPython 2.7, 3.4 and PyPy2.
"""

from geocodepy.geocoders import *  # noqa
from geocodepy.location import Location  # noqa
from geocodepy.point import Point  # noqa
from geocodepy.timezone import Timezone  # noqa
from geocodepy.util import __version__, __version_info__, get_version  # noqa

# geocodepy.geocoders.options must not be importable as `geocodepy.options`,
# because that is ambiguous (which options are that).
del options  # noqa

# `__all__` is intentionally not defined in order to not duplicate
# the same list of geocoders as in `geocodepy.geocoders` package.
