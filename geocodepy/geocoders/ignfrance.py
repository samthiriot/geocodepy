import asyncio
import csv
import os
import tempfile
from typing import override
import warnings
from functools import partial
from urllib.parse import urlencode

from geocodepy.exc import GeocoderQueryError, GeocoderServiceError
from geocodepy.geocoders.base import DEFAULT_SENTINEL, Geocoder, GeocoderWithCSVBatch
from geocodepy.location import Location
from geocodepy.util import logger

__all__ = ("IGNFrance", )


class IGNFrance(GeocoderWithCSVBatch):
    """Geocoder using the IGN France GeoCoder OpenLS API.

    Documentation at:
        https://geoservices.ign.fr/services-web-essentiels
    """

    api_path = '/geocodage'
    geocode_path = '/search'
    geocode_batch_path = '/search/csv'
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
        """  # noqa

        super().__init__(
            scheme=scheme,
            timeout=timeout,
            proxies=proxies,
            user_agent=user_agent,
            ssl_context=ssl_context,
            adapter_factory=adapter_factory,
            cache=cache,
            cache_expire=cache_expire,
            min_delay_seconds=1/49  # from the API doc: "50 requêtes par seconde"
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
        self.geocode_batch_api = (
            '%s://%s%s%s' % (self.scheme, self.domain, self.api_path, self.geocode_batch_path)
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

    def _geocode_batch_sync(self, tmp_file, indexes="address,poi", timeout=60, callback=None):
        try:
            return self._call_geocoder(
                self.geocode_batch_api,
                callback,
                timeout=timeout,
                file=tmp_file.name,
                data={"columns": "query", "indexes": indexes},
                )
        finally:
            os.unlink(tmp_file.name)
        #   "section": "",
        #   "municipalitycode": "",
        #   "number": "",
        #   "lon": "",
        #   "postcode": "",
        #   "oldmunicipalitycode": "",
        #   "citycode": "",
        #   "type": "",
        #   "result_columns": "",
        #   "districtcode": "",
        #   "category": "",
        #   "departmentcode": "",
        #   "sheet": "",
        #   "lat": "",
        #   "result_columns": "",

    async def _geocode_batch_async(self, tmp_file, indexes="address,poi", timeout=60, callback=None):
        def _callback_delete_file(*args, **kwargs):
            try:
                os.unlink(tmp_file.name)
            except Exception as e:
                print("error deleting file", e)
                raise e
            return callback(*args, **kwargs)

        return await self._call_geocoder(
            self.geocode_batch_api,
            callback,
            timeout=timeout,
            file=tmp_file.name,
            data={"columns": "query", "indexes": indexes},
            )
    
    @override
    def geocode_batch(self, addresses, indexes="address,poi", timeout=60):
        """
        IGN offers a native batch geocoding service. The list of addresses is written in a
        temporary file and sent to the geocoding service.
        """
        #return super().geocode_batch(addresses, exactly_one=exactly_one, **kwargs)
        # TODO how to skip the results in cache?
        callback = partial(self._parse_csv)
        indexes = self._parse_index(indexes)
        files = self._write_csv(addresses, max_size=1024*1024*1)  # accept 1Mb, the official limit is 50Mb
        try:
            if self._run_async:
                async def fut():
                    sem = asyncio.Semaphore(5)
                    
                    async def one(tmp_file):
                        async with sem:
                            return await self._geocode_batch_async(tmp_file, indexes, timeout, callback)
                    
                    grouped = await asyncio.gather(*(one(f) for f in files),
                                                   return_exceptions=True)

                    results = []
                    for g in grouped:
                        if isinstance(g, Exception):
                            # à toi de voir: log, accumuler, ou re-raise
                            raise g
                        results.extend(g)
                    return results

                    # TODO delete files

                return fut()
            else:
                # call sequentially the geocoding of every single file
                results = []
                for tmp_file in files:
                    results.extend(self._geocode_batch_sync(tmp_file, indexes, timeout, callback))
                return results
        finally:
            pass
            # for tmp_file in files:
            #     print("deleting file", tmp_file.name)
            #     os.unlink(tmp_file.name)

    def _parse_feature_csv(self, row, mapping):
        # print("in _parse_feature_csv, row:", row)
        
        # TODO should we keep all the columns?
        feature_dict = {
            key.replace("result_", ""): None if row[index] == "" else row[index]
            for key, index in mapping.items()
            if (key.startswith("result_") or key in ["latitude", "longitude", "query"])}

        # debug
        # for key, value in feature_dict.items():
        #     print("\t", key, ":", value)
    
        if feature_dict.get('status') != 'ok':
            return None
        del feature_dict['status']

        placename = feature_dict.get('label', None)
        # in case of POI, the service does not always return a label
        if placename is None:
            # in this case we do our best to generate something looking like an
            # address, in the form <toponym> <postcode> <city>
            placename = " ".join(e for e in [
                feature_dict.get('toponym'),
                feature_dict.get('postcode', None),
                feature_dict.get('city', None)
            ] if e is not None)

        self._check_type(feature_dict.get('type', None))

        #TODO for POI?
        # type_feature = feature_dict.get('type')
        # if not type_feature == 'Feature':
        #     raise GeocoderServiceError(
        #         "Expected a Feature as a result but received a %s" % type_feature
        #     )
        
        # Parse each resource.
        latitude = float(feature_dict.get('latitude'))
        longitude = float(feature_dict.get('longitude'))
        del feature_dict['latitude']
        del feature_dict['longitude']
        
        return Location(placename, (latitude, longitude), feature_dict)

    def _parse_csv(self, file):
        try:
            mapping = None
            with open(file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if mapping is None:
                        # use the header row to analyze the mapping
                        mapping = {column: i for i, column in enumerate(row)}
                        continue
                    # parse the feature
                    yield self._parse_feature_csv(row, mapping)
                    # TODO multiple results?
        finally:
            os.unlink(file)
            
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
        :type query: :class:`geocodepy.point.Point`, list or tuple of ``(latitude,
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

    def _check_type(self, _type):
        if _type not in {'housenumber', 'street', 'locality', 'municipality', None}:
            raise GeocoderQueryError("invalid type %s" % _type)

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
            # in this case we do our best to generate something looking like an
            # address, in the form <toponym> <postcode> <city>
            placename = " ".join(e for e in [
                properties.get('toponym'),
                properties.get('postcode', [None])[0],
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
