#
#   @brief Refinamento dos dados do csv removendo linhas sem latitude ou longitude.
#   autores : Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
#   histórico : 20250601 arquivo criado
#

import pandas as pd

def load_data(path="data/geocoded_output.csv"):
    dataframe=pd.read_csv(path)
    dataframe.dropna(subset=["LATITUDE","LONGITUDE"],inplace=True)
    return dataframe