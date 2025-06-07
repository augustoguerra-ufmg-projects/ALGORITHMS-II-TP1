import pandas as pd
from dash import Input, Output
import dash_leaflet as dl
from dash import html


def register_callbacks(app, dataframe):
    @app.callback(
        Output("layer-point-group", "children"), [Input("edit-control", "geojson")], prevent_initial_call=True
    )
    def update_points(selected_geojson):
        if not selected_geojson or not selected_geojson.get("features"):
            return []

        try:
            coords = selected_geojson["features"][-1]["geometry"]["coordinates"][0]
            lats = [c[1] for c in coords]
            lons = [c[0] for c in coords]
            min_lat, max_lat = min(lats), max(lats)
            min_lon, max_lon = min(lons), max(lons)
        except (IndexError, TypeError, KeyError):
            return []

        filter_dataframe = dataframe[
            (dataframe["LATITUDE"] >= min_lat)
            & (dataframe["LATITUDE"] <= max_lat)
            & (dataframe["LONGITUDE"] >= min_lon)
            & (dataframe["LONGITUDE"] <= max_lon)
        ]

        markers = []
        for _, row in filter_dataframe.iterrows():
            if pd.notna(row["Nome"]):  # There is a match in the CSV
                popup_content = html.Div(
                    [
                        html.Img(src=row["Link Imagem"], style={"width": "100px"}),
                        html.P(f"Nome: {row['Nome']}"),
                        html.P(f"Petisco: {row['Nome Petisco']}"),
                        html.P(f"Descrição: {row['Descricao']}"),
                        html.A("Detalhes", href=row["Link Detalhes"], target="_blank"),
                        html.P(f"Endereço: {row['Endereco']}"),
                    ]
                )
                icon = dict(
                    iconUrl="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png"
                )
            else:
                popup_content = html.Div(
                    [
                        html.P(f"Logradouro: {row['NOME_LOGRADOURO']}"),
                        html.P(
                            f"Nome Fantasia: {row['NOME_FANTASIA']}"
                            if pd.notna(row["NOME_FANTASIA"])
                            else "Nome Fantasia: Não disponível"
                        ),
                    ]
                )
                icon = dict(
                    iconUrl="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png"
                )

            markers.append(
                dl.Marker(
                    position=(row["LATITUDE"], row["LONGITUDE"]),
                    children=[
                        dl.Tooltip(
                            content=f"{row['NOME_FANTASIA'] if pd.notna(row['NOME_FANTASIA']) else row['NOME_LOGRADOURO']} Clique e saiba mais sobre o local!"
                        ),
                        dl.Popup(popup_content),
                    ],
                    icon=icon,
                )
            )
        return markers
