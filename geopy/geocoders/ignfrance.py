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
            adapter_factory=None
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

            .. versionadded:: 2.0
        """  # noqa
        
        super().__init__(
            scheme=scheme,
            timeout=timeout,
            proxies=proxies,
            user_agent=user_agent,
            ssl_context=ssl_context,
            adapter_factory=adapter_factory,
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
            This will be reset to one if ``exactly_one`` is True.

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
            indexes = index.split(',')
            illegal_indexes = set(indexes) - {'address', 'parcel', 'poi'}
            if illegal_indexes:
                raise GeocoderQueryError(
                    "Invalid index: %s. Valid indexes are: address, parcel, poi"
                    % illegal_indexes
                )
            params['index'] = ','.join(indexes)

        if type is not None:
            if type not in {'housenumber', 'street', 'locality', 'municipality'}:
                raise GeocoderQueryError("invalid type %s")
            params['type'] = type
    
        url = "?".join((self.geocode_api, urlencode(params)))

        logger.debug("%s.geocode: %s", self.__class__.__name__, url)
        callback = partial(self._parse_json, exactly_one=exactly_one)
        return self._call_geocoder(url, callback, timeout=timeout)

    def reverse(
            self,
            query,
            *,
            reverse_geocode_preference=('StreetAddress', ),
            maximum_responses=25,
            filtering='',
            exactly_one=True,
            timeout=DEFAULT_SENTINEL
    ):
        """
        Return an address by location point.

        :param query: The coordinates for which you wish to obtain the
            closest human-readable addresses.
        :type query: :class:`geopy.point.Point`, list or tuple of ``(latitude,
            longitude)``, or string as ``"%(latitude)s, %(longitude)s"``.

        :param list reverse_geocode_preference: Enable to set expected results
            type. It can be `StreetAddress` or `PositionOfInterest`.
            Default is set to `StreetAddress`.

        :param int maximum_responses: The maximum number of responses
            to ask to the API in the query body.

        :param str filtering: Provide string that help setting geocoder
            filter. It contains an XML string. See examples in documentation
            and ignfrance.py file in directory tests.

        :param bool exactly_one: Return one result or a list of results, if
            available.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geopy.exc.GeocoderTimedOut`
            exception. Set this only if you wish to override, on this call
            only, the value set during the geocoder's initialization.

        :rtype: ``None``, :class:`geopy.location.Location` or a list of them, if
            ``exactly_one=False``.

        """

        sub_request = """
            <ReverseGeocodeRequest>
                {reverse_geocode_preference}
                <Position>
                  <gml:Point>
                    <gml:pos>{query}</gml:pos>
                  </gml:Point>
                  {filtering}
                </Position>
            </ReverseGeocodeRequest>
        """

        xml_request = self.xml_request.format(
            method_name='ReverseGeocodeRequest',
            sub_request=sub_request,
            maximum_responses=maximum_responses
        )

        for pref in reverse_geocode_preference:
            if pref not in ('StreetAddress', 'PositionOfInterest'):
                raise GeocoderQueryError(
                    '`reverse_geocode_preference` must contain '
                    'one or more of: StreetAddress, PositionOfInterest'
                )

        point = self._coerce_point_to_string(query, "%(lat)s %(lon)s")
        reverse_geocode_preference = '\n'.join(
            '<ReverseGeocodePreference>%s</ReverseGeocodePreference>' % pref
            for pref
            in reverse_geocode_preference
        )

        request_string = xml_request.format(
            maximum_responses=maximum_responses,
            query=point,
            reverse_geocode_preference=reverse_geocode_preference,
            filtering=filtering
        )

        url = "?".join((self.api, urlencode({'xls': request_string})))

        logger.debug("%s.reverse: %s", self.__class__.__name__, url)
        callback = partial(
            self._parse_xml,
            exactly_one=exactly_one,
            is_reverse=True,
            is_freeform='false'
        )
        return self._request_raw_content(url, callback, timeout=timeout)

    def _parse_xml(self,
                   page,
                   is_reverse=False,
                   is_freeform=False,
                   exactly_one=True):
        """
        Returns location, (latitude, longitude) from XML feed
        and transform to json
        """
        # Parse the page
        tree = ET.fromstring(page.encode('utf-8'))

        # Clean tree from namespace to facilitate XML manipulation
        def remove_namespace(doc, namespace):
            """Remove namespace in the document in place."""
            ns = '{%s}' % namespace
            nsl = len(ns)
            for elem in doc.iter():
                if elem.tag.startswith(ns):
                    elem.tag = elem.tag[nsl:]

        remove_namespace(tree, 'http://www.opengis.net/gml')
        remove_namespace(tree, 'http://www.opengis.net/xls')
        remove_namespace(tree, 'http://www.opengis.net/xlsext')

        # Return places as json instead of XML
        places = self._xml_to_json_places(tree, is_reverse=is_reverse)

        if not places:
            return None
        if exactly_one:
            return self._parse_place(places[0], is_freeform=is_freeform)
        else:
            return [
                self._parse_place(
                    place,
                    is_freeform=is_freeform
                ) for place in places
            ]

    def _xml_to_json_places(self, tree, is_reverse=False):
        """
        Transform the xml ElementTree due to XML webservice return to json
        """

        select_multi = (
            'GeocodedAddress'
            if not is_reverse
            else 'ReverseGeocodedLocation'
        )

        adresses = tree.findall('.//' + select_multi)
        places = []

        sel_pl = './/Address/Place[@type="{}"]'
        for adr in adresses:
            el = {}
            el['pos'] = adr.find('./Point/pos')
            el['street'] = adr.find('.//Address/StreetAddress/Street')
            el['freeformaddress'] = adr.find('.//Address/freeFormAddress')
            el['municipality'] = adr.find(sel_pl.format('Municipality'))
            el['numero'] = adr.find(sel_pl.format('Numero'))
            el['feuille'] = adr.find(sel_pl.format('Feuille'))
            el['section'] = adr.find(sel_pl.format('Section'))
            el['departement'] = adr.find(sel_pl.format('Departement'))
            el['commune_absorbee'] = adr.find(sel_pl.format('CommuneAbsorbee'))
            el['commune'] = adr.find(sel_pl.format('Commune'))
            el['insee'] = adr.find(sel_pl.format('INSEE'))
            el['qualite'] = adr.find(sel_pl.format('Qualite'))
            el['territoire'] = adr.find(sel_pl.format('Territoire'))
            el['id'] = adr.find(sel_pl.format('ID'))
            el['id_tr'] = adr.find(sel_pl.format('ID_TR'))
            el['bbox'] = adr.find(sel_pl.format('Bbox'))
            el['nature'] = adr.find(sel_pl.format('Nature'))
            el['postal_code'] = adr.find('.//Address/PostalCode')
            el['extended_geocode_match_code'] = adr.find(
                './/ExtendedGeocodeMatchCode'
            )

            place = {}

            def testContentAttrib(selector, key):
                """
                Helper to select by attribute and if not attribute,
                value set to empty string
                """
                return selector.attrib.get(
                    key,
                    None
                ) if selector is not None else None

            place['accuracy'] = testContentAttrib(
                adr.find('.//GeocodeMatchCode'), 'accuracy')

            place['match_type'] = testContentAttrib(
                adr.find('.//GeocodeMatchCode'), 'matchType')

            place['building'] = testContentAttrib(
                adr.find('.//Address/StreetAddress/Building'), 'number')

            place['search_centre_distance'] = testContentAttrib(
                adr.find('.//SearchCentreDistance'), 'value')

            for key, value in iter(el.items()):
                if value is not None:
                    place[key] = value.text
                else:
                    place[key] = None

            # We check if lat lng is not empty and unpack accordingly
            if place['pos']:
                lat, lng = place['pos'].split(' ')
                place['lat'] = lat.strip()
                place['lng'] = lng.strip()
            else:
                place['lat'] = place['lng'] = None

            # We removed the unused key
            place.pop("pos", None)
            places.append(place)

        return places

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
        
        print(feature)

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
