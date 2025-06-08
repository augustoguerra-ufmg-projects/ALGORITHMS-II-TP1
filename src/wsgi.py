from app import app, server  # or whatever your main file is named
from callbacks.map_callbacks import register_callbacks
from layout import layout
from utils.data_loader import load_data

app.layout = layout
register_callbacks(app, load_data())

application = server

if __name__ == "__main__":
    app.run(debug=True)
