from geocodepy.geocoders import IGNFrance

import logging

from geocodepy.geocoders.nominatim import Nominatim

logging.basicConfig(level=logging.INFO)

geocoder = IGNFrance(cache=False)

addresses_france = [
    "55 Rue du Faubourg Saint-Honoré, 75008 Paris, France", 
    "Elysée, Paris",
    "13 Rue de la Paix, 75002 Paris, France",
    "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER",
    "1 Pl. de la Comédie, 69001 Lyon, France"
]
# geocode an address
results = geocoder.geocode_batch(addresses_france)

for result in results:
    print("[%s %s]\t %s" % (result.latitude, result.longitude, result.address))


geocoder = Nominatim(user_agent='geocodepy-example-2', cache=True)

# geocode an address
results = geocoder.geocode_batch(addresses_france)

for result in results:
    print("[%s %s]\t %s" % (result.latitude, result.longitude, result.address))


geocoder = Nominatim(user_agent='geocodepy-example-1', cache=False)
for address in addresses_france:
    result = geocoder.geocode(address)
    print("[%s %s]\t %s" % (result.latitude, result.longitude, result.address))
