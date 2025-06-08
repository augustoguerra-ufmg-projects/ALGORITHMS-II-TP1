import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import html, Dash, Input, Output
import pandas as pd

import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "build"))
from kdtree import KDTree

# carrega os dados e constrói a kd tree
df = pd.read_csv("../data/data.csv")
pairs = [((row["lat"], row["lon"]), idx) for idx, row in df.iterrows()]
tree = KDTree(pairs)

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
                cluster=True,
            )
        ],
        style={'width': '100%', 'height': '100%'}
    )
], style={'position': 'fixed', 'width': '100%', 'height': '100%', 'top': 0, 'left': 0})

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
            "tooltip": data.get("nome_fantasia")
        })
    return dlx.dicts_to_geojson(res)

server = app.server
