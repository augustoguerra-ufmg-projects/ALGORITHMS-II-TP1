import pandas as pd

def load_data(path="data/geocoded_output.csv"):
    dataframe=pd.read_csv(path)
    dataframe.dropna(subset=["LATITUDE","LONGITUDE"],inplace=True)
    return dataframe