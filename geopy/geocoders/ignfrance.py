import warnings
from functools import partial
from urllib.parse import urlencode

from geopy.exc import GeocoderQueryError, GeocoderServiceError
from geopy.geocoders.base import DEFAULT_SENTINEL, Geocoder
from geopy.location import Location
from geopy.util import logger

__all__ = ("IGNFrance", )


class IGNFrance(Geocoder):
    """Geocoder using the IGN France GeoCoder OpenLS API.

    Documentation at:
        https://geoservices.ign.fr/services-web-essentiels
    """

    api_path = '/geocodage'
    geocode_path = '/search'
    reverse_path = '/reverse'

    def __init__(
            self,
            api_key=None,
            *,
            username=None,
            password=None,
            referer=None,
            domain='data.geopf.fr',
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

        :param str api_key: Not used.

            .. deprecated:: 2.3
                IGNFrance geocoding methods no longer accept or require
                authentication, see `<https://geoservices.ign.fr/actualites/2021-10-04-evolution-des-modalites-dacces-aux-services-web>`_.
                This parameter is scheduled for removal in geopy 3.0.

        :param str username: Not used.

            .. deprecated:: 2.3
                See the `api_key` deprecation note.

        :param str password: Not used.

            .. deprecated:: 2.3
                See the `api_key` deprecation note.

        :param str referer: Not used.

            .. deprecated:: 2.3
                See the `api_key` deprecation note.

        :param str domain: Currently it is ``'wxs.ign.fr'``, can
            be changed for testing purposes for developer API
            e.g ``'gpp3-wxs.ign.fr'`` at the moment.

        :param str scheme:
            See :attr:`geopy.geocoders.options.default_scheme`.

        :param int timeout:
            See :attr:`geopy.geocoders.options.default_timeout`.

        :param dict proxies:
            See :attr:`geopy.geocoders.options.default_proxies`.

        :param str user_agent:
            See :attr:`geopy.geocoders.options.default_user_agent`.

        :type ssl_context: :class:`ssl.SSLContext`
        :param ssl_context:
            See :attr:`geopy.geocoders.options.default_ssl_context`.

        :param callable adapter_factory:
            See :attr:`geopy.geocoders.options.default_adapter_factory`.

        :param bool cache:
            Either True or None to activate cache, or False to disable it.
            Default is None. 
            If a a :class:`diskcache.Cache` instance is passed, it will be used as is.

        :param int cache_expire:
            Time, in seconds, to keep a cached result in memory. 
            Enables to query again the geocoder in case its database, or algorithm, has changed.
            Default is 30 days.
        
            .. versionadded:: 2.0
        """  # noqa
        
        super().__init__(
            scheme=scheme,
            timeout=timeout,
            proxies=proxies,
            user_agent=user_agent,
            ssl_context=ssl_context,
            adapter_factory=adapter_factory,
            cache=cache,
            cache_expire=cache_expire
        )

        if api_key or username or password or referer:
            warnings.warn(
                "IGNFrance no longer accepts or requires authentication, "
                "so api_key, username, password and referer are not used "
                "anymore. These arguments should be removed. "
                "In geopy 3 these options will be removed, causing "
                "an error instead of this warning.",
                DeprecationWarning,
                stacklevel=2,
            )

        self.domain = domain.strip('/')
        self.geocode_api = (
            '%s://%s%s%s' % (self.scheme, self.domain, self.api_path, self.geocode_path)
        )
        self.reverse_api = (
            '%s://%s%s%s' % (self.scheme, self.domain, self.api_path, self.reverse_path)
        )

    def geocode(
            self,
            query,
            *,
            limit=None,
            index='address',
            type=None,
            exactly_one=True,
            timeout=DEFAULT_SENTINEL
    ):
        """
        Return a location point by address.

        :param str query: The address or query you wish to geocode.

        :param int limit: Defines the maximum number of items in the
            response structure. If not provided and there are multiple
            results the BAN API will return 10 results by default.

        :param str index: The index to use for the geocoding.
            It can be `address` for postal address, `parcel` for cadastral 
            parcel, `poi` for point of interest. You can also combine them
            with a comma.
            Default is set to `address`.

        :param str type: The type to use for address index. Can be `housenumber`,
            `street`, `locality`, `municipality`

        :param bool exactly_one: Return one result or a list of results, if
            available.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geopy.exc.GeocoderTimedOut`
            exception. Set this only if you wish to override, on this call
            only, the value set during the geocoder's initialization.

        :rtype: ``None``, :class:`geopy.location.Location` or a list of them, if
            ``exactly_one=False``.

        """

        params = {
            'q': query,
        }

        if limit is not None:
            params["limit"] = limit
        
        if index is not None:
            indexes = self._parse_index(index)
            params['index'] = ','.join(indexes)

        if type is not None:
            self._check_type(type)
            params['type'] = type
    
        url = "?".join((self.geocode_api, urlencode(params)))

        logger.debug("%s.geocode: %s", self.__class__.__name__, url)
        callback = partial(self._parse_json, exactly_one=exactly_one)
        return self._call_geocoder(url, callback, timeout=timeout)

    def reverse(
            self,
            query,
            *,
            index='address',
            type=None,
            limit=25,
            exactly_one=True,
            timeout=DEFAULT_SENTINEL
    ):
        """
        Return an address by location point.

        :param query: The coordinates for which you wish to obtain the
            closest human-readable addresses.
        :type query: :class:`geopy.point.Point`, list or tuple of ``(latitude,
            longitude)``, or string as ``"%(latitude)s, %(longitude)s"``.

        :param str index: The index to use for the geocoding.
            It can be `address` for postal address, `parcel` for cadastral 
            parcel, `poi` for point of interest. You can also combine them
            with a comma.
            Default is set to `address`.

        :param str type: The type to use for address index. Can be `housenumber`,
            `street`, `locality`, `municipality`

        :param int limit: Defines the maximum number of items in the
            response structure. If not provided and there are multiple
            results the BAN API will return 10 results by default.

        :param bool exactly_one: Return one result or a list of results, if
            available.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geopy.exc.GeocoderTimedOut`
            exception. Set this only if you wish to override, on this call
            only, the value set during the geocoder's initialization.

        :rtype: ``None``, :class:`geopy.location.Location` or a list of them, if
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

        if index is not None:
            indexes = self._parse_index(index)
            params['index'] = ','.join(indexes)

        if type is not None:
            self._check_type(type)
            params['type'] = type

        if limit is not None:
            params["limit"] = limit    
        
        url = "?".join((self.reverse_api, urlencode(params)))
        logger.debug("%s.reverse: %s", self.__class__.__name__, url)
        callback = partial(self._parse_json, exactly_one=exactly_one)
        return self._call_geocoder(url, callback, timeout=timeout)


    def _parse_index(self, index):
        indexes = index.split(',')
        illegal_indexes = set(indexes) - {'address', 'parcel', 'poi'}
        if illegal_indexes:
            raise GeocoderQueryError(
                "Invalid index: %s. Valid indexes are: address, parcel, poi"
                % illegal_indexes
            )
        return indexes

    def _check_type(self, type):
        if type not in {'housenumber', 'street', 'locality', 'municipality'}:
            raise GeocoderQueryError("invalid type %s")

    def _request_raw_content(self, url, callback, *, timeout):
        """
        Send the request to get raw content.
        """
        return self._call_geocoder(
            url,
            callback,
            timeout=timeout,
            is_json=False,
        )

    def _parse_feature(self, feature):
        
        type_feature = feature.get('type')
        if not type_feature == 'Feature':
            raise GeocoderServiceError(
                "Expected a Feature as a result but received a %s" % type_feature
            )
        # Parse each resource.
        geometry = feature.get('geometry', {})
        latitude = geometry.get('coordinates', [])[1]
        longitude = geometry.get('coordinates', [])[0]
        
        properties = feature.get('properties', {})
        placename = properties.get('label', None)
        # in case of POI, the service does not always return a label
        if placename is None:
            # in this case we do our best to generate something looking like an address, in the form <toponym> <postcode> <city>
            placename = " ".join(e for e in [
                properties.get('toponym'),
                properties.get('postcode',[None])[0],
                properties.get('city', [None])[0]
                ] if e is not None)
            
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
