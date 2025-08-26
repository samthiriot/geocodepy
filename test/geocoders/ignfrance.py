import pytest

from geopy.exc import GeocoderQueryError
from geopy.geocoders import IGNFrance
from test.geocoders.util import BaseTestGeocoder
from test.proxy_server import ProxyServerThread


class TestIGNFrance(BaseTestGeocoder):

    @classmethod
    def make_geocoder(cls, **kwargs):
        return IGNFrance(
            timeout=10
        )

    async def test_user_agent_custom(self):
        geocoder = IGNFrance(
            user_agent='my_user_agent/1.0'
        )
        assert geocoder.headers['User-Agent'] == 'my_user_agent/1.0'


    async def test_geocode_parcel(self):
        await self.geocode_run(
            {"query": "44109000EX0114",
             "index": "parcel"},
            {"latitude": 47.222482, "longitude": -1.556303},
        )

    async def test_geocode_no_result(self):
        await self.geocode_run(
            {"query": 'asdfasdfasdf'},
            {},
            expect_failure=True,
        )

    async def test_reverse_no_result(self):
        await self.reverse_run(
            # North Atlantic Ocean
            {"query": (35.173809, -37.485351)},
            {},
            expect_failure=True
        )

    async def test_geocode_with_address(self):
        await self.geocode_run(
            {"query": "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER"},
            {"latitude": 47.293048,
             "longitude": 1.718985,
             "address": "Le Camp des Landes 41200 Villefranche-sur-Cher"},
        )

    async def test_geocode_with_address_index(self):
        await self.geocode_run(
            {"query": "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER",
             "index": "address"},
            {"latitude": 47.293048,
             "longitude": 1.718985,
             "address": "Le Camp des Landes 41200 Villefranche-sur-Cher"},
        )

    async def test_geocode_with_poi1(self):
        """Tests the presidential palais (stable location). Expected result 
        does contain the postcode and city"""
        await self.geocode_run(
            {"query": "Elysée, Paris",
             "index": "poi"},
            {"latitude": 48.86931,
             "longitude": 2.316138,
             "address": "Palais de l'Élysée 75008 Paris"},
        )

    async def test_geocode_with_poi2(self):
        """tests a port (stable location, but the name might change later)
        Expected result does not contain the city"""
        await self.geocode_run(
            {"query": "port de dunkerque",
             "index": "poi"},
            {"latitude": 51.061641,
             "longitude": 2.348728,
             "address": "Rade de Dunkerque"},
        )

    async def test_geocode_with_type_housenumber(self):
        """tests the type parameter housenumber"""
        res = await self.geocode_run(
            {"query": "13 Rue de la Paix, 75002 Paris, France",
             "index": "address",
             "type": "housenumber"},
            {},
        )
        assert res.raw.get('type') == 'Feature'
        assert res.raw.get('properties').get('type') == 'housenumber'
        assert int(res.raw.get('properties').get('housenumber')) == 13
        
    async def test_geocode_with_type_street(self):
        """tests the type parameter street"""
        res = await self.geocode_run(
            {"query": "13 Rue de la Paix, 75002 Paris, France",
             "index": "address",
             "type": "street"},
            {},
        )
        assert res.raw.get('type') == 'Feature'
        assert res.raw.get('properties').get('type') == 'street'
        
    async def test_geocode_with_type_locality(self):
        """tests the type parameter street"""
        res = await self.geocode_run(
            {"query": "Paris, France",
             "index": "address",
             "type": "locality"},
            {},
        )
        print(res)
        assert res.raw.get('type') == 'Feature'
        assert res.raw.get('properties').get('type') == 'locality'

    async def test_geocode_with_type_municipality(self):
        """tests the type parameter street"""
        res = await self.geocode_run(
            {"query": "Paris, France",
             "index": "address",
             "type": "municipality"},
            {},
        )
        assert res.raw.get('type') == 'Feature'
        assert res.raw.get('properties').get('type') == 'municipality'

    async def test_geocode_poi_multiple_results5(self):
        """test the respect of limit"""
        res = await self.geocode_run(
            {"query": "plage Marseille",
             "index": "poi",
             "limit": 5,
             "exactly_one": False},
            {},
        )
        assert len(res) == 5

    async def test_geocode_poi_multiple_results3(self):
        """test the respect of limit"""
        res = await self.geocode_run(
            {"query": "plage Marseille",
             "index": "poi",
             "limit": 3,
             "exactly_one": False},
            {},
        )
        assert len(res) == 3

    async def test_reverse_default(self):
        res = await self.reverse_run(
            {"query": '48.86931,2.316138'},
            {},
        )
        assert res.address == '9 Rue de l\'Elysée 75008 Paris'

    async def test_reverse_index_address(self):
        res = await self.reverse_run(
            {"query": '48.86931,2.316138', "index": "address"},
            {},
        )
        assert res.address == '9 Rue de l\'Elysée 75008 Paris'

    async def test_reverse_index_address_type_housenumber(self):
        res = await self.reverse_run(
            {"query": '48.86931,2.316138', "index": "address", "type": "housenumber"},
            {},
        )
        assert res.address == '9 Rue de l\'Elysée 75008 Paris'

    async def test_reverse_index_address_type_street(self):
        res = await self.reverse_run(
            {"query": '48.86931,2.316138', "index": "address", "type": "street"},
            {},
        )
        assert res.address == 'Rue de l\'Elysée 75008 Paris,Paris 8e Arrondissement'

    async def test_reverse_index_poi(self):
        res = await self.reverse_run(
            {"query": '48.86931,2.316138', "index": "poi"},
            {},
        )
        assert res.address == 'Palais de l\'Élysée 75008 Paris'


    async def test_reverse_invalid_preference(self):
        with pytest.raises(GeocoderQueryError):
            self.geocoder.reverse(
                query='47.229554,-1.541519',
                index='a'  # invalid
            )

class TestIGNFranceUsernameAuthProxy(BaseTestGeocoder):
    proxy_timeout = 5

    @classmethod
    def make_geocoder(cls, **kwargs):
        return IGNFrance(
            timeout=10,
            **kwargs
        )

    @pytest.fixture(scope='class', autouse=True)
    async def start_proxy(_, request, class_geocoder):
        cls = request.cls
        cls.proxy_server = ProxyServerThread(timeout=cls.proxy_timeout)
        cls.proxy_server.start()
        cls.proxy_url = cls.proxy_server.get_proxy_url()
        async with cls.inject_geocoder(cls.make_geocoder(proxies=cls.proxy_url)):
            yield
        cls.proxy_server.stop()
        cls.proxy_server.join()

    async def test_proxy_is_respected(self):
        assert 0 == len(self.proxy_server.requests)
        await self.geocode_run(
            {"query": "Elysée, Paris",
             "index": "poi"},
            {"latitude": 48.86931,
             "longitude": 2.316138,
             "address": "Palais de l'Élysée 75008 Paris"},
        )
        assert 1 == len(self.proxy_server.requests)
