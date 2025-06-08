import pandas as pd
import utm

df = pd.read_csv("20250401_atividade_economica.csv", sep=";", encoding="utf-8")

keywords = ["BAR", "RESTAURANTE"]

mask = (
    df["DESCRICAO_CNAE_PRINCIPAL"].str.upper()
    .str.contains("|".join(keywords), na=False)
)
df = df[mask]

# converte os pontos UTM para latitude/longitude
def parse(s):
    tokens = s.replace('(', '').replace(')', '').split()
    x = float(tokens[1])
    y = float(tokens[2])
    return [x, y]

coords = df["GEOMETRIA"].apply(parse).apply(pd.Series)
lat, lon = utm.to_latlon(coords[0], coords[1], 23, northern=False)
df["LATITUDE"] = lat
df["LONGITUDE"] = lon

# formata os endereços
def endereco(row):
    logradouro = row["DESC_LOGRADOURO"] + " " + row["NOME_LOGRADOURO"]
    numero = row["NUMERO_IMOVEL"]
    bairro = row["NOME_BAIRRO"]
    complemento = row["COMPLEMENTO"]
    return f"{logradouro}, {numero} {complemento} - {bairro}"

df["ENDERECO_COMPLETO"] = df.apply(endereco, axis=1)

# cruza os dados do comida de buteco
df = df.merge(
    pd.read_csv("comida_di_buteco.csv"),
    left_on="ID_ATIV_ECON_ESTABELECIMENTO",
    right_on="ID",
    how="left"
)

# seleciona e renomeia colunas
columns = {
    "NOME_FANTASIA": "nome_fantasia",
    "NOME": "nome",
    "ENDERECO_COMPLETO": "endereco",
    "DATA_INICIO_ATIVIDADE": "inicio",
    "IND_POSSUI_ALVARA": "alvara",
    "LATITUDE": "lat",
    "LONGITUDE": "lon",
    "Link Detalhes": "link",
    "Nome Petisco": "petisco",
    "Link Imagem": "imagem"
}

df = df.rename(columns=columns)[[*columns.values()]]
df.to_csv("data.csv", index=False)
