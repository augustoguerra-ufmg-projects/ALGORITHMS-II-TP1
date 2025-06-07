from dash import html
from components.map_component import create_map

center_bh = (-19.912998, -43.940933)
zoom_bh = 12
bounds_bh = [[-20.048, -44.079], [-19.784, -43.800]]

layout = html.Div(
    [
        create_map(center_bh, zoom_bh, bounds_bh),
        html.Div(id="points-info"),
        html.H3("Orthogonal Range Search in Belo Horizonte using KD-Tree data structure")
    ]
)
