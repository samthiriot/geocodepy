from functools import partial
from urllib.parse import urlencode

from geocodepy.geocoders.base import DEFAULT_SENTINEL, Geocoder
from geocodepy.location import Location
from geocodepy.util import logger

__all__ = ("BANFrance", )


class BANFrance(Geocoder):
    """Geocoder using the Base Adresse Nationale France API.

    Documentation at:
        https://adresse.data.gouv.fr/api
    """

    geocode_path = '/search'
    reverse_path = '/reverse'

    def __init__(
            self,
            *,
            domain='api-adresse.data.gouv.fr',
            scheme=None,
            timeout=DEFAULT_SENTINEL,
            proxies=DEFAULT_SENTINEL,
            user_agent=None,
            ssl_context=DEFAULT_SENTINEL,
            adapter_factory=None,
            cache=None,
            cache_expire=None
    ):
        """

        :param str domain: Currently it is ``'api-adresse.data.gouv.fr'``, can
            be changed for testing purposes.

        :param str scheme:
            See :attr:`geocodepy.geocoders.options.default_scheme`.

        :param int timeout:
            See :attr:`geocodepy.geocoders.options.default_timeout`.

        :param dict proxies:
            See :attr:`geocodepy.geocoders.options.default_proxies`.

        :param str user_agent:
            See :attr:`geocodepy.geocoders.options.default_user_agent`.

        :type ssl_context: :class:`ssl.SSLContext`
        :param ssl_context:
            See :attr:`geocodepy.geocoders.options.default_ssl_context`.

        :param callable adapter_factory:
            See :attr:`geocodepy.geocoders.options.default_adapter_factory`.

        :param bool cache:
            Either True or None to activate cache, or False to disable it.
            Default is None.
            If a a :class:`diskcache.Cache` instance is passed, it will be used as is.

        :param int cache_expire:
            Time, in seconds, to keep a cached result in memory.
            Enables to query again the geocoder in case its database, or algorithm,
            has changed. Default is 30 days.

            .. versionadded:: 2.0

        """
        super().__init__(
            scheme=scheme,
            timeout=timeout,
            proxies=proxies,
            user_agent=user_agent,
            ssl_context=ssl_context,
            adapter_factory=adapter_factory,
            cache=cache,
            cache_expire=cache_expire,
            min_delay_seconds=1 / 50
        )
        self.domain = domain.strip('/')

        self.geocode_api = (
            '%s://%s%s' % (self.scheme, self.domain, self.geocode_path)
        )
        self.reverse_api = (
            '%s://%s%s' % (self.scheme, self.domain, self.reverse_path)
        )

    def geocode(
            self,
            query,
            *,
            limit=None,
            exactly_one=True,
            timeout=DEFAULT_SENTINEL
    ):
        """
        Return a location point by address.

        :param str query: The address or query you wish to geocode.

        :param int limit: Defines the maximum number of items in the
            response structure. If not provided and there are multiple
            results the BAN API will return 5 results by default.
            This will be reset to one if ``exactly_one`` is True.

        :param bool exactly_one: Return one result or a list of results, if
            available.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geocodepy.exc.GeocoderTimedOut`
            exception. Set this only if you wish to override, on this call
            only, the value set during the geocoder's initialization.

        :rtype: ``None``, :class:`geocodepy.location.Location` or a list of them, if
            ``exactly_one=False``.

        """

        params = {
            'q': query,
        }

        if limit is not None:
            params['limit'] = limit

        url = "?".join((self.geocode_api, urlencode(params)))

        logger.debug("%s.geocode: %s", self.__class__.__name__, url)
        callback = partial(self._parse_json, exactly_one=exactly_one)
        return self._call_geocoder(url, callback, timeout=timeout)

    def reverse(
            self,
            query,
            *,
            exactly_one=True,
            timeout=DEFAULT_SENTINEL
    ):
        """
        Return an address by location point.

        :param query: The coordinates for which you wish to obtain the
            closest human-readable addresses.
        :type query: :class:`geocodepy.point.Point`, list or tuple of ``(latitude,
            longitude)``, or string as ``"%(latitude)s, %(longitude)s"``.

        :param bool exactly_one: Return one result or a list of results, if
            available.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geocodepy.exc.GeocoderTimedOut`
            exception. Set this only if you wish to override, on this call
            only, the value set during the geocoder's initialization.

        :rtype: ``None``, :class:`geocodepy.location.Location` or a list of them, if
            ``exactly_one=False``.

        """

        try:
            lat, lon = self._coerce_point_to_string(query).split(',')
        except ValueError:
            raise ValueError("Must be a coordinate pair or Point")

        params = {
            'lat': lat,
            'lon': lon,
        }

        url = "?".join((self.reverse_api, urlencode(params)))
        logger.debug("%s.reverse: %s", self.__class__.__name__, url)
        callback = partial(self._parse_json, exactly_one=exactly_one)
        return self._call_geocoder(url, callback, timeout=timeout)

    def _parse_feature(self, feature):
        # Parse each resource.
        latitude = feature.get('geometry', {}).get('coordinates', [])[1]
        longitude = feature.get('geometry', {}).get('coordinates', [])[0]
        placename = feature.get('properties', {}).get('label')
        # postcode = feature.get('properties', {}).get('postcode')

        return Location(placename, (latitude, longitude), feature)

    def _parse_json(self, response, exactly_one):
        if response is None or 'features' not in response:
            return None
        features = response['features']
        if not len(features):
            return None
        if exactly_one:
            return self._parse_feature(features[0])
        else:
            return [self._parse_feature(feature) for feature in features]
