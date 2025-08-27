from geopy.geocoders import IGNFrance

import logging

from geopy.geocoders.nominatim import Nominatim

logging.basicConfig(level=logging.INFO)

geocoder = IGNFrance(cache=False)

# geocode an address
results = geocoder.geocode_batch(
    ["55 Rue du Faubourg Saint-Honoré, 75008 Paris, France", 
    "Elysée, Paris",
    "13 Rue de la Paix, 75002 Paris, France",
    "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER",
    "1 Pl. de la Comédie, 69001 Lyon, France"])

for result in results:
    print("[%s %s]\t %s" % (result.latitude, result.longitude, result.address))


geocoder = Nominatim(user_agent='geocodepy-example', cache=True)

# geocode an address
results = geocoder.geocode_batch(
    ["55 Rue du Faubourg Saint-Honoré, 75008 Paris, France", 
    "Elysée, Paris",
    "13 Rue de la Paix, 75002 Paris, France",
    "Camp des Landes, 41200 VILLEFRANCHE-SUR-CHER",
    "1 Pl. de la Comédie, 69001 Lyon, France"])

for result in results:
    print("[%s %s]\t %s\t %s" % (result.latitude, result.longitude, result.address, repr(result.raw)))