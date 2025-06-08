#
#   @brief Refinamento dos dados do csv removendo linhas sem latitude ou longitude.
#   autores : Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
#   histórico : 20250601 arquivo criado
#

import pandas as pd


def load_data(path="data/geocoded_output.csv"):
    df = pd.read_csv(path)
    df.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)

    comida_df = pd.read_csv("data/comida_di_buteco.csv")

    merged = df.merge(comida_df, left_on="ID_ATIV_ECON_ESTABELECIMENTO", right_on="ID", how="left")

    return merged
