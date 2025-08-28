from geocodepy.geocoders.base import DEFAULT_SENTINEL
from geocodepy.geocoders.tomtom import TomTom

__all__ = ("AzureMaps", )


class AzureMaps(TomTom):
    """AzureMaps geocoder based on TomTom.

    Documentation at:
        https://docs.microsoft.com/en-us/azure/azure-maps/index
    """

    geocode_path = '/search/address/json'
    reverse_path = '/search/address/reverse/json'

    def __init__(
            self,
            subscription_key,
            *,
            scheme=None,
            timeout=DEFAULT_SENTINEL,
            proxies=DEFAULT_SENTINEL,
            user_agent=None,
            ssl_context=DEFAULT_SENTINEL,
            adapter_factory=None,
            domain='atlas.microsoft.com',
            cache=None,
            cache_expire=None
    ):
        """
        :param str subscription_key: Azure Maps subscription key.

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

            .. versionadded:: 2.0

        :param str domain: Domain where the target Azure Maps service
            is hosted.

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
            api_key=subscription_key,
            scheme=scheme,
            timeout=timeout,
            proxies=proxies,
            user_agent=user_agent,
            ssl_context=ssl_context,
            adapter_factory=adapter_factory,
            domain=domain,
            cache=cache,
            cache_expire=cache_expire
        )

    def _geocode_params(self, formatted_query):
        return {
            'api-version': '1.0',
            'subscription-key': self.api_key,
            'query': formatted_query,
        }

    def _reverse_params(self, position):
        return {
            'api-version': '1.0',
            'subscription-key': self.api_key,
            'query': position,
        }
