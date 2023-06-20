import dash
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__)
app.title = "my title"

app.layout = html.Div(html.H2("This is my app"))

def plot_map(path):
    us_cities = pd.read_csv(path)
    
    fig = px.scatter_mapbox(us_cities, lat="latitude", lon="longitude", hover_name="sensor_id",
                            color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig.show()

if __name__=='__main__':
    app.run_server(debug=True, port=8001)