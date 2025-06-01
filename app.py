import dash
from dash import html, Input, Output
import dash_leaflet as dl
import pandas as pd

# Carregar os dados do CSV
try:
    df = pd.read_csv("geocoded_output.csv")
    # Remover linhas com valores ausentes em LATITUDE ou LONGITUDE
    df.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
except FileNotFoundError:
    print("Arquivo 'geocoded_output.csv' não encontrado. Crie um arquivo de exemplo.")
    raise FileNotFoundError("Certifique-se de que o arquivo 'geocoded_output.csv' está no diretório correto.")

# Coordenadas aproximadas do centro de Belo Horizonte e zoom inicial
center_bh = (-19.912998, -43.940933)
zoom_bh = 12

# Limites aproximados para Belo Horizonte (para restringir a visualização, se desejado)
bounds_bh = [
    [-20.048, -44.079],  # Sudoeste
    [-19.784, -43.800],  # Nordeste
]

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Bares e Restaurantes de Belo Horizonte"),
        dl.Map(
            id="mapa-bh",
            center=center_bh,
            zoom=zoom_bh,
            style={"width": "100%", "height": "90vh"},
            children=[
                dl.TileLayer(),
                dl.FeatureGroup(
                    [
                        dl.EditControl(
                            id="edit-control",
                            draw={
                                "rectangle": True,  # Apenas retângulo
                                "polygon": False,  # Polígono também (retângulo é um tipo de polígono)
                                "circle": False,  # Habilita círculo
                                "polyline": False,
                                "marker": False,
                                "circlemarker": False,
                            },
                            edit={"edit": False, "remove": True},  # Permitir remover, não editar
                        )
                    ]
                ),
                dl.LayerGroup(id="layer-group-pontos"),  # Camada para os pontos filtrados
            ],
            bounds=bounds_bh,  # Limites do mapa para restringir a visualização
            maxBounds=bounds_bh,  # Limites máximos do mapa
        ),
        html.Div(id="info-pontos"),
    ]
)


@app.callback(Output("layer-group-pontos", "children"), [Input("edit-control", "geojson")], prevent_initial_call=True)
def atualizar_pontos(geojson_selecionado):
    if not geojson_selecionado or not geojson_selecionado["features"]:
        return []

    # Pega a geometria da última área desenhada
    try:
        coords = geojson_selecionado["features"][-1]["geometry"]["coordinates"][0]

        # Obter os limites da área selecionada (min/max lat/lon)
        lats = [coord[1] for coord in coords]
        lons = [coord[0] for coord in coords]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

    except (IndexError, TypeError, KeyError) as e:
        print(f"Erro ao processar geojson: {e}")
        return []

    # ==========================================================
    # TODO : Implementar a lógica de filtragem de pontos com a KD-Tree
    # Filtrar o DataFrame para pontos dentro da área selecionada
    df_filtrado = df[
        (df["LATITUDE"] >= min_lat)
        & (df["LATITUDE"] <= max_lat)
        & (df["LONGITUDE"] >= min_lon)
        & (df["LONGITUDE"] <= max_lon)
    ]

    # Criar marcadores para os pontos filtrados
    marcadores = []
    for _, row in df_filtrado.iterrows():
        marcadores.append(
            dl.Marker(
                position=(row["LATITUDE"], row["LONGITUDE"]),
                children=[
                    dl.Tooltip(content=f"{row['NOME_LOGRADOURO']} / {row['NOME_FANTASIA']}"),
                    dl.Popup(
                        html.Div(
                            [
                                html.P(f"Logradouro: {row['NOME_LOGRADOURO']}"),
                                html.P(f"Nome Fantasia: {row['NOME_FANTASIA']}"),
                            ]
                        )
                    ),
                ],
            )
        )
    return marcadores


if __name__ == "__main__":
    app.run(debug=True)
