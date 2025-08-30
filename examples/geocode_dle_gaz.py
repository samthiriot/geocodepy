import pandas

from geocodepy.geocoders import IGNFrance
from geocodepy.geocoders import Nominatim

from geocodepy.geocoders.banfrance import BANFrance


import logging

logging.basicConfig(level=logging.INFO)

# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1

sample_size = 100
res_file = "/tmp/dle_gaz_2023_geocoded.xlsx"

print("reading sample of", sample_size, "addresses")
df = pandas.read_csv("examples/data/dle_gaz_2023.csv",
                     sep=";",
                     #nrows=100,
                     header=0,
                     skiprows=1,  # ignore the first row of header
                     usecols=["ADRESSE", "NOM_COMMUNE"]
                     ).sample(n=sample_size, random_state=42)
df["query"] = df["ADRESSE"] + ", " + df["NOM_COMMUNE"]
#print(df)


def geocode_dataframe(df, geocoder):
    results = geocoder.geocode_batch(df["query"])

    df["label"] = [result.address if result is not None else None
                   for result in results]
    df["latitude"] = [float(result.latitude) if result is not None else None
                      for result in results]
    df["longitude"] = [float(result.longitude) if result is not None else None
                       for result in results]

    decoded_raw = pandas.DataFrame.from_records([
        {key: value for key, value in result.raw.items() if key not in ["properties"]}
        if result is not None else {}
        for result in results])
    
    has_properties = False
    for result in results:
        if result is None or result.raw is None:
            continue
        has_properties = "properties" in result.raw
        break

    df.reset_index(drop=True, inplace=True)
    if has_properties:
        decoded_properties = pandas.DataFrame.from_records([
            result.raw["properties"]
            if result is not None else {}
            for result in results])
        return pandas.concat([df, decoded_raw, decoded_properties],
                             axis=1, join='outer')
    else:
        return pandas.concat([df, decoded_raw],
                             axis=1, join='outer')

with pandas.ExcelWriter(res_file) as writer:

    print("exporting sample...")
    df.to_excel(writer, sheet_name="sample")

    print("geocoding with BAN...")
    results = geocode_dataframe(df, BANFrance())
    print("exporting BAN results...")
    results.to_excel(writer, sheet_name="BAN")

    print("geocoding with IGN...")
    results = geocode_dataframe(df, IGNFrance())
    print("exporting IGN results...")
    results.to_excel(writer, sheet_name="IGN")

    print("geocoding with Nominatim...")
    results = geocode_dataframe(df, Nominatim(user_agent="geocodepy-test-batch"))
    print("exporting Nominatim results...")
    results.to_excel(writer, sheet_name="Nominatim")


print("exported in", res_file)
