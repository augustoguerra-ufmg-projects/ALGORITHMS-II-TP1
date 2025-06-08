import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
from dash import html, Dash, Input, Output
import pandas as pd

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../build"))
from kdtree import KDTree

# carrega os dados e constrói a kd tree
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/data.csv"))
pairs = [((row["lat"], row["lon"]), idx) for idx, row in df.iterrows()]
tree = KDTree(pairs)

marker = assign("""
    function(feature, latlng) {
        let black = new L.Icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });
        
        let red = new L.Icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        });

        return L.marker(latlng, {icon: feature.properties.comida_di_buteco ? red : black});
    }
""")

# configura o dash
app = Dash(__name__, prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map(
        center=[-19.9245, -43.9352],
        zoom=13,
        children=[
            dl.TileLayer(),
            dl.FeatureGroup([
                dl.EditControl(
                    id="edit-control",
                    draw={
                        "rectangle": True,
                        "polyline": False,
                        "polygon": False,
                        "circle": False,
                        "marker": False,
                        "circlemarker": False
                    }
                )
            ]),
            dl.GeoJSON(
                id="geojson-layer",
                data=dlx.dicts_to_geojson([]),
                pointToLayer=marker,
                cluster=True,
                superClusterOptions={
                    "radius": 60,
                    "maxZoom": 15,
                    "minPoints": 5
                }
            )
        ],
        style={'width': '100%', 'height': '100%'}
    )
], style={'position': 'fixed', 'width': '100%', 'height': '100%', 'top': 0, 'left': 0})

def tooltip(data):
    return data.nome_fantasia if not pd.isna(data.nome_fantasia) else data.nome

def popup(data):
    res = f"""
        <h5>{tooltip(data)}</h5>
        <p>Endereço: {data.endereco}</p>
        <p>Início das atividades: {data.inicio}</p>
        <p>Alvará: {data.alvara}</p>
    """

    if not pd.isna(data.link):
        res += f"""
            <hr>
            <br>
            <a href="{data.link}">Link no comida di buteco</a>
            <p>Prato: {data.petisco}</p>
            <img src="{data.imagem}" width="256px">
        """

    return res

@app.callback(Output("geojson-layer", "data"), Input("edit-control", "geojson"), prevent_initial_call=True)
def update(selection):
    if not selection or not selection.get("features"):
        return dlx.dicts_to_geojson([])
    
    points = set()
    for feature in selection["features"]:
        coords = feature["geometry"]["coordinates"][0]
        lats = [c[1] for c in coords]
        lons = [c[0] for c in coords]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        
        for _, idx in tree.search((min_lat, min_lon), (max_lat, max_lon)):
            points.add(idx)

    res = []
    for idx in points:
        data = df.loc[idx]
        res.append({
            "lat": data["lat"],
            "lon": data["lon"],
            "comida_di_buteco": not pd.isna(data["link"]),
            "tooltip": tooltip(data),
            "popup": popup(data)
        })
    return dlx.dicts_to_geojson(res)

if __name__ == "__main__":
    app.run(debug=True)
