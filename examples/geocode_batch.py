from http.client import HTTPConnection
from geocodepy.geocoders import IGNFrance
from geocodepy.geocoders.geoapify import Geoapify
from geocodepy.geocoders.nominatim import Nominatim


import logging
logging.basicConfig(level=logging.INFO)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

from http.client import HTTPConnection

HTTPConnection.debuglevel = 1

geocoder = IGNFrance(cache=False)
geocoder = Geoapify(api_key="290b1d1a2b9f4882a7ff83d35ad994f7")

addresses_france = [
    "55 Rue du Faubourg Saint-Honoré, 75008 Paris, France", 
    "Elysée, Paris",
    "13 Rue de la Paix, 75002 Paris, France",
    "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER",
    "1 Pl. de la Comédie, 69001 Lyon, France"
]


def gen_many_addresses(max):
    for i in range(max):
        for address in addresses_france:
            yield address


# geocode an address
results = geocoder.geocode_batch(addresses_france)
for i, result in enumerate(results):
    print("\n", i, repr(result))
    if result is not None:
        print("\t", result.raw)
#     #print("[%s %s]\t %s" % (result., result.longitude, result.address))

# càmparaison: 
# sans batch: (throtteling) 1.6min ; 4.43m!!!
#
# avec batch: 13s
#
quit()

results = geocoder.geocode_batch(gen_many_addresses(10000))

for result in results:
    print("[%s %s]\t %s" % (result.latitude, result.longitude, result.address))

quit()

geocoder = Nominatim(user_agent='geocodepy-example-2', cache=True)

# geocode an address
results = geocoder.geocode_batch(addresses_france)

for result in results:
    print("[%s %s]\t %s" % (result.latitude, result.longitude, result.address))


geocoder = Nominatim(user_agent='geocodepy-example-1', cache=False)
for address in addresses_france:
    result = geocoder.geocode(address)
    print("[%s %s]\t %s" % (result.latitude, result.longitude, result.address))
