from geocodepy.geocoders.base import DEFAULT_SENTINEL
from geocodepy.geocoders.nominatim import Nominatim

__all__ = ("OpenMapQuest", )


class OpenMapQuest(Nominatim):
    """Geocoder using MapQuest Open Platform Web Services.

    Documentation at:
        https://developer.mapquest.com/documentation/open/

    MapQuest provides two Geocoding APIs:

    - :class:`geocodepy.geocoders.OpenMapQuest` (this class) Nominatim-alike API
      which is based on Open data from OpenStreetMap.
    - :class:`geocodepy.geocoders.MapQuest` MapQuest's own API which is based on
      Licensed data.
    """

    geocode_path = '/nominatim/v1/search'
    reverse_path = '/nominatim/v1/reverse'

    def __init__(
            self,
            api_key,
            *,
            timeout=DEFAULT_SENTINEL,
            proxies=DEFAULT_SENTINEL,
            domain='open.mapquestapi.com',
            scheme=None,
            user_agent=None,
            ssl_context=DEFAULT_SENTINEL,
            adapter_factory=None,
            cache=None,
            cache_expire=None
    ):
        """

        :param str api_key: API key provided by MapQuest, required.

        :param int timeout:
            See :attr:`geocodepy.geocoders.options.default_timeout`.

        :param dict proxies:
            See :attr:`geocodepy.geocoders.options.default_proxies`.

        :param str domain: Domain where the target Nominatim service
            is hosted.

        :param str scheme:
            See :attr:`geocodepy.geocoders.options.default_scheme`.

        :param str user_agent:
            See :attr:`geocodepy.geocoders.options.default_user_agent`.

        :type ssl_context: :class:`ssl.SSLContext`
        :param ssl_context:
            See :attr:`geocodepy.geocoders.options.default_ssl_context`.

        :param callable adapter_factory:
            See :attr:`geocodepy.geocoders.options.default_adapter_factory`.

            .. versionadded:: 2.0

        :param bool cache:
            Either True or None to activate cache, or False to disable it.
            Default is None. 
            If a a :class:`diskcache.Cache` instance is passed, it will be used as is.

        :param int cache_expire:
            Time, in seconds, to keep a cached result in memory. 
            Enables to query again the geocoder in case its database, or algorithm, has changed.
            Default is 30 days.
        
            .. versionadded:: 2.0
        """
        super().__init__(
            timeout=timeout,
            proxies=proxies,
            domain=domain,
            scheme=scheme,
            user_agent=user_agent,
            ssl_context=ssl_context,
            adapter_factory=adapter_factory,
            cache=cache,
            cache_expire=cache_expire
        )
        self.api_key = api_key

    def _construct_url(self, base_api, params):
        """
        Construct geocoding request url. Overridden.

        :param str base_api: Geocoding function base address - self.api
            or self.reverse_api.

        :param dict params: Geocoding params.

        :return: string URL.
        """
        params['key'] = self.api_key
        return super()._construct_url(base_api, params)
