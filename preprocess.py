import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import json
import os

# 0 json para armazenar requests ja realizadas

cache_path="geocache.json"
if os.path.exists(cache_path):
    with open(cache_path,"r",encoding="utf-8") as f:
        geocache=json.load(f)
else:
    geocache={}

# 1 aplica filtro com database local com base nas keywords

keywords=['BAR','RESTAURANTE']

original_database="20250401_atividade_economica.csv"
original_dataframe=pd.read_csv(original_database,sep=';',encoding='utf-8')

filt=original_dataframe['DESCRICAO_CNAE_PRINCIPAL'].str.upper().str.contains('|'.join(keywords),na=False)
dataframe=original_dataframe[filt]
print("Filtrou estabelecimentos")
print(f"Total filtrado: {len(dataframe)}")

# 2 utiliza a API do OpenStretMaps para salvar a latitude e a longitude com base no endereco

latitudes=[]
longitudes=[]

def complete_address(row):
    logradouro = f"{str(row.get('DESC_LOGRADOURO', '')).strip()} {str(row.get('NOME_LOGRADOURO', '')).strip()}"
    description=[str(row.get('NUMERO_IMOVEL', '')).strip(), str(row.get('NOME_BAIRRO', '')).strip(), "Belo Horizonte", "MG", "Brasil"]
    return(', '.join(i for i in description if i))

dataframe['ENDERECO_COMPLETO']=dataframe.apply(complete_address,axis=1)

geolocator=Nominatim(user_agent="tp1_geocoder")
geocode=RateLimiter(geolocator.geocode,min_delay_seconds=1,max_retries=2,error_wait_seconds=2, swallow_exceptions=False)

for i, address in enumerate(dataframe['ENDERECO_COMPLETO']):
    if address in geocache:
        lat,lon=geocache[address]
        print(f"[{i+1}/{len(dataframe)}] Cache: {address}")
    else:
        try:
            location=geocode(address, timeout=10)
            if location:
                lat,lon=location.latitude,location.longitude
            else:
                lat,lon=None,None
        except Exception as e:
            print(f"Erro linha {i}: {e}")
            lat,lon=None,None
        
        geocache[address]=[lat,lon]
        #debug
        print(f"[{i+1}/{len(dataframe)}] Request: {address}")
    latitudes.append(lat)
    longitudes.append(lon)

with open(cache_path,"w",encoding="utf-8") as f:
    json.dump(geocache,f,ensure_ascii=False,indent=2)

dataframe['LATITUDE']=latitudes
dataframe['LONGITUDE']=longitudes
print('Adicionou latitude e longitude')

# 3 faz projecao apenas dos dados importantes
# data de inicio das atividades, se tem alvará de funcionamento, endereço, nome e (ou nome fantasia)

projection=['ID_ATIV_ECON_ESTABELECIMENTO', 'DATA_INICIO_ATIVIDADE', 'IND_POSSUI_ALVARA', 'ENDERECO_COMPLETO', 'NOME', 'NOME_FANTASIA', 'LATITUDE', 'LONGITUDE']
dataframe=dataframe[projection]
print("Projecao realizada")

dataframe.to_csv("dataframe.csv", index=False, sep=';', encoding='utf-8')