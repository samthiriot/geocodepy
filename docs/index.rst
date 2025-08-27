Welcome to GeoPy's documentation!
=================================

.. image:: _static/logo-wide.png
   :width: 80%
   :align: center
   :alt: GeoPy logo

:Documentation: https://geocodepy.readthedocs.io/
:Source Code: https://github.com/geopy/geopy
:Stack Overflow: https://stackoverflow.com/questions/tagged/geopy
:GIS Stack Exchange: https://gis.stackexchange.com/questions/tagged/geopy
:Discussions: https://github.com/geopy/geopy/discussions
:Issue Tracker: https://github.com/geopy/geopy/issues
:PyPI: https://pypi.org/project/geopy/

.. automodule:: geopy
   :members: __doc__

.. toctree::
    :maxdepth: 3
    :caption: Contents

    index


Installation
~~~~~~~~~~~~

::

    pip install geopy

Geocoders
~~~~~~~~~

.. automodule:: geocodepy.geocoders
   :members: __doc__

Accessing Geocoders
-------------------

The typical way of retrieving a geocoder class is to make an import
from ``geocodepy.geocoders`` package::

    from geocodepy.geocoders import Nominatim

.. autofunction:: geocodepy.geocoders.get_geocoder_for_service

Default Options Object
----------------------

.. autoclass:: geocodepy.geocoders.options
   :members:
   :undoc-members:

Usage with Pandas
-----------------

It is possible to geocode a pandas DataFrame with geopy, however,
rate-limiting must be taken into account.

A large number of DataFrame rows might produce a significant amount of
geocoding requests to a Geocoding service, which might be throttled
by the service (e.g. by returning `Too Many Requests` 429 HTTP error
or timing out).

:mod:`geocodepy.extra.rate_limiter` classes provide a convenient
wrapper, which can be used to automatically add delays between geocoding
calls to reduce the load on the Geocoding service. Also it can retry
failed requests and swallow errors for individual rows.

If you're having the `Too Many Requests` error, you may try the following:

- Use :mod:`geocodepy.extra.rate_limiter` with non-zero
  ``min_delay_seconds``.
- Try a different Geocoding service (please consult with their ToS first,
  as some services prohibit bulk geocoding).
- Take a paid plan on the chosen Geocoding service, which provides
  higher quota.
- Provision your own local copy of the Geocoding service (such as Nominatim).

Rate Limiter
++++++++++++

.. automodule:: geocodepy.extra.rate_limiter
   :members: __doc__

.. autoclass:: geocodepy.extra.rate_limiter.RateLimiter

   .. automethod:: __init__

.. autoclass:: geocodepy.extra.rate_limiter.AsyncRateLimiter

   .. automethod:: __init__

ArcGIS
------

.. autoclass:: geocodepy.geocoders.ArcGIS
   :members:

   .. automethod:: __init__

AzureMaps
---------

.. autoclass:: geocodepy.geocoders.AzureMaps
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__

Baidu
-----

.. autoclass:: geocodepy.geocoders.Baidu
   :members:

   .. automethod:: __init__

BaiduV3
-------

.. autoclass:: geocodepy.geocoders.BaiduV3
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__

BANFrance
---------

.. autoclass:: geocodepy.geocoders.BANFrance
   :members:

   .. automethod:: __init__

Bing
----

.. autoclass:: geocodepy.geocoders.Bing
   :members:

   .. automethod:: __init__

DataBC
------

.. autoclass:: geocodepy.geocoders.DataBC
   :members:

   .. automethod:: __init__

GeocodeEarth
------------

.. autoclass:: geocodepy.geocoders.GeocodeEarth
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__

GeocodeFarm
-----------

.. versionchanged:: 2.2
   This class has been removed, because the service is too unreliable.
   See :issue:`445`.

Geocodio
--------

.. autoclass:: geocodepy.geocoders.Geocodio
   :members:

   .. automethod:: __init__

Geokeo
------------

.. autoclass:: geocodepy.geocoders.Geokeo
   :members:

   .. automethod:: __init__

Geolake
--------

.. autoclass:: geocodepy.geocoders.Geolake
   :members:

   .. automethod:: __init__

GeoNames
--------

.. autoclass:: geocodepy.geocoders.GeoNames
   :members:

   .. automethod:: __init__

GoogleV3
--------

.. autoclass:: geocodepy.geocoders.GoogleV3
   :members:

   .. automethod:: __init__

HERE
----

.. autoclass:: geocodepy.geocoders.Here
   :members:

   .. automethod:: __init__

HEREv7
------

.. autoclass:: geocodepy.geocoders.HereV7
   :members:

   .. automethod:: __init__

IGNFrance
---------

.. autoclass:: geocodepy.geocoders.IGNFrance
   :members:

   .. automethod:: __init__

MapBox
--------

.. autoclass:: geocodepy.geocoders.MapBox
   :members:

   .. automethod:: __init__

MapQuest
--------

.. autoclass:: geocodepy.geocoders.MapQuest
   :members:

   .. automethod:: __init__

MapTiler
--------

.. autoclass:: geocodepy.geocoders.MapTiler
   :members:

   .. automethod:: __init__

OpenCage
--------

.. autoclass:: geocodepy.geocoders.OpenCage
   :members:

   .. automethod:: __init__

OpenMapQuest
------------

.. autoclass:: geocodepy.geocoders.OpenMapQuest
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__

Nominatim
---------

.. autoclass:: geocodepy.geocoders.Nominatim
   :members:

   .. automethod:: __init__

Pelias
------

.. autoclass:: geocodepy.geocoders.Pelias
   :members:

   .. automethod:: __init__

Photon
------

.. autoclass:: geocodepy.geocoders.Photon
   :members:

   .. automethod:: __init__

PickPoint
---------

.. autoclass:: geocodepy.geocoders.PickPoint
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__

LiveAddress
-----------

.. autoclass:: geocodepy.geocoders.LiveAddress
   :members:

   .. automethod:: __init__

TomTom
------

.. autoclass:: geocodepy.geocoders.TomTom
   :members:

   .. automethod:: __init__

What3Words
----------

.. autoclass:: geocodepy.geocoders.What3Words
   :members:

   .. automethod:: __init__

What3WordsV3
------------

.. autoclass:: geocodepy.geocoders.What3WordsV3
   :members:

   .. automethod:: __init__

Woosmap
------------

.. autoclass:: geocodepy.geocoders.Woosmap
   :members:

   .. automethod:: __init__

Yandex
------

.. autoclass:: geocodepy.geocoders.Yandex
   :members:

   .. automethod:: __init__

Calculating Distance
~~~~~~~~~~~~~~~~~~~~

.. automodule:: geocodepy.distance
   :members: __doc__

.. autofunction:: geocodepy.distance.lonlat

.. autoclass:: geocodepy.distance.Distance
   :members: __init__, destination

.. autoclass:: geocodepy.distance.geodesic
   :show-inheritance:

.. autoclass:: geocodepy.distance.great_circle
   :show-inheritance:

Data
~~~~

.. autoclass:: geocodepy.location.Location
    :members: address, latitude, longitude, altitude, point, raw

.. autoclass:: geocodepy.point.Point
    :members:

    .. automethod:: __new__

.. autoclass:: geocodepy.timezone.Timezone
    :members: pytz_timezone, raw

Units Conversion
~~~~~~~~~~~~~~~~

.. automodule:: geocodepy.units
    :members:

Exceptions
~~~~~~~~~~

.. autoclass:: geocodepy.exc.GeopyError
    :show-inheritance:

.. autoclass:: geocodepy.exc.ConfigurationError
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderServiceError
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderQueryError
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderQuotaExceeded
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderRateLimited
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderAuthenticationFailure
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderInsufficientPrivileges
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderTimedOut
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderUnavailable
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderParseError
    :show-inheritance:

.. autoclass:: geocodepy.exc.GeocoderNotFound
    :show-inheritance:

Adapters
~~~~~~~~

.. automodule:: geocodepy.adapters
    :members: __doc__

Supported Adapters
------------------

.. autoclass:: geocodepy.adapters.RequestsAdapter
    :show-inheritance:

.. autoclass:: geocodepy.adapters.URLLibAdapter
    :show-inheritance:

.. autoclass:: geocodepy.adapters.AioHTTPAdapter
    :show-inheritance:


Base Classes
------------

.. autoclass:: geocodepy.adapters.AdapterHTTPError
    :show-inheritance:

    .. automethod:: __init__

.. autoclass:: geocodepy.adapters.BaseAdapter
    :members:

    .. automethod:: __init__

.. autoclass:: geocodepy.adapters.BaseSyncAdapter
    :show-inheritance:
    :members:

.. autoclass:: geocodepy.adapters.BaseAsyncAdapter
    :show-inheritance:
    :members:

Logging
~~~~~~~

geopy will log geocoding URLs with a logger name ``geopy`` at level `DEBUG`,
and for some geocoders, these URLs will include authentication information.

HTTP bodies of responses with unsuccessful status codes are logged
with `INFO` level.

Default logging level is `NOTSET`, which delegates the messages processing to
the root logger. See docs for :meth:`logging.Logger.setLevel` for more
information.


Semver
~~~~~~

geopy attempts to follow semantic versioning, however some breaking changes
are still being made in minor releases, such as:

- Backwards-incompatible changes of the undocumented API. This shouldn't
  affect anyone, unless they extend geocoder classes or use undocumented
  features or monkey-patch anything. If you believe that something is
  missing in geopy, please consider opening an issue or providing
  a patch/PR instead of hacking around geocodepy.

- Geocoding services sometimes introduce new APIs and deprecate the previous
  ones. We try to upgrade without breaking the geocoder's API interface,
  but the :attr:`geocodepy.location.Location.raw` value might change in a
  backwards-incompatible way.

- Behavior for invalid input and peculiar edge cases might be altered.
  For example, :class:`geocodepy.point.Point` instances previously did
  coordinate values normalization, though it's not documented, and it was
  completely wrong for the latitudes outside the `[-90; 90]` range.
  So instead of using an incorrectly normalized value for latitude,
  a :class:`ValueError` exception is now thrown (:issue:`294`).

Features and usages being phased out are covered with deprecation :mod:`warnings`
when possible. Make sure to run your python with the ``-Wd`` switch to see
if your code emits the warnings.

To make the upgrade less painful, please read the changelog before upgrading.


Changelog
~~~~~~~~~

:doc:`Changelog for 2.x.x series <changelog_2xx>`.

:doc:`Changelog for 1.x.x series <changelog_1xx>`.

:doc:`Changelog for 0.9x series <changelog_09x>`.


Indices and search
==================

* :ref:`genindex`
* :ref:`search`

