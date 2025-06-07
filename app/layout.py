from dash import html
from components.map_component import create_map

center_bh = (-19.912998, -43.940933)
zoom_bh = 12
bounds_bh = [[-20.048, -44.079], [-19.784, -43.800]]

layout = html.Div(
    [
        html.H1("Belo Horizonte Orthogonal Range Search KD-Tree"),
        create_map(center_bh, zoom_bh, bounds_bh),
        html.Div(id="points-info"),
    ]
)
