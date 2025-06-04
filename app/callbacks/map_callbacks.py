#
#   @brief Realiza a busca ortogonal no mapa utilizando a KD-Tree implementada
#   autores : Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
#   histórico : 20250601 arquivo criado
#

from dash import Input, Output
import dash_leaflet as dl
from dash import html

def register_callbacks(app,dataframe):
    @app.callback(
        Output("layer-point-group","children"),
        [Input("edit-control","geojson")],
        prevent_initial_call=True
    )

    def update_points(selected_geojson):
        if not selected_geojson or not selected_geojson["features"]:
            return []
        
        try:
            coords=selected_geojson["features"][-1]["geometry"]["coordinates"][0]
            lats=[c[1] for c in coords]
            lons=[c[0] for c in coords]
            min_lat,max_lat=min(lats),max(lats)
            min_lon,max_lon=min(lons),max(lons)
        except (IndexError, TypeError, KeyError):
            return []

        #==============================================================================
        # TODO: Implementar a filtragem utilizando a KD-Tree
        #
        #==============================================================================
        filter_dataframe=dataframe[
            (dataframe["LATITUDE"]>=min_lat)&(dataframe["LATITUDE"]<=max_lat)&
            (dataframe["LONGITUDE"]>=min_lon)&(dataframe["LONGITUDE"]<=max_lon)
        ]

        return[
            dl.Marker(
                position=(row["LATITUDE"],row["LONGITUDE"]),
                children=[
                    dl.Tooltip(content=f"{row['NOME_LOGRADOURO']} / {row['NOME_FANTASIA']}"),
                    dl.Popup(html.Div([
                        html.P(f"Logradouro: {row['NOME_LOGRADOURO']}"),
                        html.P(f"Nome Fantasia: {row['NOME_FANTASIA']}")
                    ]))
                ]
            )
            for _, row in filter_dataframe.iterrows()
        ]  