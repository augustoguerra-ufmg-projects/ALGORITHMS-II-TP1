#
#   @brief Construcao de mapa com dash_leaflet library para plotar o mapa de Belo Horizonte
#   autores : Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
#   histórico : 20250601 arquivo criado
#

import dash_leaflet as dl


def create_map(center, zoom, bounds):
    return dl.Map(
        id="bh-map",
        center=center,
        zoom=zoom,
        bounds=bounds,
        maxBounds=bounds,
        children=[
            dl.TileLayer(),
            dl.FeatureGroup(
                [
                    dl.EditControl(
                        id="edit-control",
                        draw={
                            "rectangle": True,
                            "polygon": False,
                            "circle": False,
                            "polyline": False,
                            "marker": False,
                            "circlemarker": False,
                        },
                        edit={"edit": False, "remove": True},
                    )
                ]
            ),
            dl.LayerGroup(id="layer-point-group"),
        ],
    )
