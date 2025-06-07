from dash import html
from app import app
from components.map_component import create_map
from callbacks.map_callbacks import register_callbacks
from utils.data_loader import load_data
import os

center_bh = (-19.912998, -43.940933)
zoom_bh = 12
bounds_bh = [[-20.048, -44.079], [-19.784, -43.800]]
dataframe = load_data()

app.layout = html.Div(
    [
        html.H1("Belo Horizonte Orthogonal Range Search KD-Tree"),
        create_map(center_bh, zoom_bh, bounds_bh),
        html.Div(id="points-info"),
    ]
)

register_callbacks(app, dataframe)

if __name__ == "__main__":
    debug = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
    app.run(debug=debug)
