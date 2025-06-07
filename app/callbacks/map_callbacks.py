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
                        html.Img(src=row["Link Imagem"], className="popup-img"),
                        html.P(f"Nome: {row['Nome']}",  className="popup-title"),
                        html.P(f"Petisco: {row['Nome Petisco']}", className="popup-sub"),
                        html.P(f"Descrição: {row['Descricao']}", className="popup-desc"),
                        html.A("Detalhes", href=row["Link Detalhes"], target="_blank", className="popup-link"),
                        html.P(f"Endereço: {row['Endereco']}", className="popup-footer"),
                    ],className="popup-card"
                )
                icon = dict(   
                iconUrl="/assets/beaf.webp",
                iconSize=[30, 41],
                iconAnchor=[15, 41],
                popupAnchor=[0, -41]
                )
            else:
                popup_content = html.Div(
                [
                    html.P(f"Logradouro: {row['NOME_LOGRADOURO']}", className="popup-title"),
                    html.P(
                    f"Nome Fantasia: {row['NOME_FANTASIA']}" if pd.notna(row["NOME_FANTASIA"]) else "Nome Fantasia: Não disponível",
                    className="popup-sub"
                ),
                ],
                className="popup-card"
                )
                icon = dict(
                    iconUrl="/assets/rawbeaf.webp",
                    iconSize=[30, 41],
                    iconAnchor=[15, 41],
                    popupAnchor=[0, -41]
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
