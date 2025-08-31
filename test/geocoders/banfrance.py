from geocodepy.geocoders import BANFrance
from test.geocoders.util import BaseTestGeocoder


class TestBANFrance(BaseTestGeocoder):

    @classmethod
    def make_geocoder(cls, **kwargs):
        return BANFrance(timeout=10, cache=False, **kwargs)

    async def test_user_agent_custom(self):
        geocoder = BANFrance(
            user_agent='my_user_agent/1.0',
            cache=False
        )
        assert geocoder.headers['User-Agent'] == 'my_user_agent/1.0'

    async def test_geocode_with_address(self):
        location = await self.geocode_run(
            {"query": "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER"},
            {"latitude": 47.293048, "longitude": 1.718985},
        )
        assert "Camp des Landes" in location.address

    async def test_reverse(self):
        location = await self.reverse_run(
            {"query": "48.154587,3.221237"},
            {"latitude": 48.154587, "longitude": 3.221237},
        )
        assert "Collemiers" in location.address

    async def test_geocode_limit(self):
        result = await self.geocode_run(
            {"query": "8 bd du port", "limit": 2, "exactly_one": False},
            {}
        )
        assert 2 >= len(result)

    async def test_geocode_batch_addresses(self):

        test_data = {
            "13 Rue de la Paix, 75002 Paris, France": {
                "latitude": 48.86931,
                "longitude": 2.316138,
                "address": "13 Rue de la Paix 75002 Paris"},
            "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER": {
                "latitude": 47.293048,
                "longitude": 1.718985,
                "address": "Le Camp des Landes 41200 Villefranche-sur-Cher"},
            "1 Pl. de la Comédie, 69001 Lyon, France": {
                "latitude": 45.767808,
                "longitude": 4.835757,
                "address": "1 Place de la Comédie 69001 Lyon"},
            "Palais de l'élysée, Paris": {
                "latitude": 48.869397,
                "longitude": 2.31688,
                "address": "Rue de l'Elysée 75008 Paris"},
        }

        results = await self.geocode_batch_run(
            {"addresses": test_data.keys()},
            test_data.values())

        assert len(results) == len(test_data)
