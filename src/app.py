from dash import Dash

app = Dash(
    __name__,
    title="k-dEats",  # Sets the browser tab title
    update_title="Loading...",
)
server = app.server
