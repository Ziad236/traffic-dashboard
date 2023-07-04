import dash
import pandas as pd
import plotly.express as px
from dash import html,dcc
from datetime import date
import plotly.graph_objects as go
from dash import html
import dash_bootstrap_components as dbc
from dash import Dash, html, dash_table, Output, Input

from main_2 import *
from benchmark import *
from app_zid import app

navy=html.Div([
            dcc.Location(id="url"),
            dbc.NavbarSimple(
            children=[
            dbc.NavItem(
            [
                html.Img(src="/assets/giza.png", className="image-giza")
            ]
        ),
                dbc.NavItem(dbc.NavLink("Home", href="/",class_name="navigation-list",id="home-link")
                            ,class_name="navigation-list"),
                dbc.NavItem(dbc.NavLink("Benchmark", href="/benchmark",
                                        class_name="navigation-list",id="benchmark-link")
                            ,class_name="navigation-list"),
                    ],
                    color='inherit',
                    brand_href="/"
                  ,class_name="background-style"
                ),html.Div(id="page-content")
],className="background-style") 


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return home
    elif pathname == "/benchmark":
        return bench_layout
    else:
        return html.H1("404 - Page not found")

@app.callback(
    Output("home-link", "active"),
    [Input("url", "pathname")]
)
def update_active_links(pathname):
    if pathname == "/":
        return True, False
    elif pathname == "/benchmark":
        return False, True
    else:
        return False, False
    
app.layout = dbc.Container(navy,fluid=True)
if __name__ == '__main__':
    app.run_server(debug=False,port=8009)