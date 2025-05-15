import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os
import concurrent.futures

# Aplica filtro com database local com base nas keywords

keywords = ["BAR", "RESTAURANTE"]

original_database = "20250401_atividade_economica.csv"
original_dataframe = pd.read_csv(original_database, sep=";", encoding="utf-8")

filt = (
    original_dataframe["DESCRICAO_CNAE_PRINCIPAL"]
    .str.upper()
    .str.contains("|".join(keywords), na=False)
)
dataframe = original_dataframe[filt]
print("Filtrou estabelecimentos")
print(f"Total filtrado: {len(dataframe)}")

latitudes = []
longitudes = []


def complete_address(row):
    description = [
        str(row.get("NUMERO_IMOVEL", "")).strip(),
        str(row.get("NOME_BAIRRO", "")).strip(),
        "Belo Horizonte",
        "MG",
        "Brasil",
    ]
    return ", ".join(i for i in description if i)


dataframe["ENDERECO_COMPLETO"] = dataframe.apply(complete_address, axis=1)

# Setup geocoder and rate limiter
geolocator = Nominatim(user_agent="tp1_geocoder")
geocode = RateLimiter(
    geolocator.geocode, min_delay_seconds=1, max_retries=2, error_wait_seconds=2
)

# Optional: Load cache from file if exists
cache_file = "cache.csv"
if os.path.exists(cache_file):
    cache_df = pd.read_csv(cache_file)
    cache = dict(
        zip(cache_df["address"], zip(cache_df["latitude"], cache_df["longitude"]))
    )
else:
    cache = {}


# Function to get location with cache
def get_location_with_cache(address):
    if address in cache:
        return cache[address]
    try:
        location = geocode(address, timeout=10)
        if location:
            coords = (location.latitude, location.longitude)
        else:
            coords = (None, None)
    except Exception as e:
        print(f"Erro com o endereço '{address}': {e}")
        coords = (None, None)
    cache[address] = coords
    return coords


# Process addresses
latitudes = []
longitudes = []

addresses = dataframe["ENDERECO_COMPLETO"].tolist()


def process_address(address):
    lat, lon = get_location_with_cache(address)
    return lat, lon


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(process_address, addresses))

for i, (lat, lon) in enumerate(results):
    latitudes.append(lat)
    longitudes.append(lon)
    print(f"[{i + 1}/{len(addresses)}] {addresses[i]} → ({lat}, {lon})")

# Append results to dataframe
dataframe["LATITUDE"] = latitudes
dataframe["LONGITUDE"] = longitudes

# Save updated cache
cache_df = pd.DataFrame(
    [(addr, lat, lon) for addr, (lat, lon) in cache.items()],
    columns=["address", "latitude", "longitude"],
)
cache_df.to_csv(cache_file, index=False)

# Save result
dataframe.to_csv("geocoded_output.csv", index=False)
