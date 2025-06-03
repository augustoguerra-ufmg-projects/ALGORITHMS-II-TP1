import dash_leaflet as dl
from dash import html

def create_map(center,zoom,bounds):
    return dl.Map(
        id="bh-map",
        center=center,
        zoom=zoom,
        bounds=bounds,
        maxBounds=bounds,

        children=[
            dl.TileLayer(),
            dl.FeatureGroup([
                dl.EditControl(
                    
                    id="edit-control",
                    draw={"rectangle": True,
                          "polygon": False, 
                          "circle": False, 
                          "polyline": False,
                          "marker": False, 
                          "circlemarker": False},
                    
                    edit={"edit": False, 
                          "remove": True},
                )
            ]),
            dl.LayerGroup(id="layer-point-group")
        ]
    )