import dash
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
from app_zid import app

from utility import create_sorted_bar_plot,Benchmark,defult_graph,size_inferance,Forcast_Benshmark

bay_comp=pd.read_csv(r'./dataset/bay_comp.csv')
metr_comp=pd.read_csv(r'./dataset/metra_comp.csv')

data_canada = px.data.gapminder().query("country == 'Canada'")
fig = px.bar(data_canada, x='year', y='pop')
metric = 'MAE'

card_content = [
    dbc.CardHeader("Model details"),
    dbc.CardBody(
        [
            html.H5("Random forest regressor", className="card-title", id="card-title"),
            html.P(
                "The system employs multiple models for each sensor, with each model having multiple outputs for forecasting at 10, 30, and 60-minute intervals. These models are compressed using the joblib library with a compression level of 6.",
                className="card-text", id="card-text"
            ),
        ]
    ),
]

bench_layout = dbc.Container([
    html.Br(),
    html.H5("Benchmark",className="graph-header"),
    html.Div([html.H6('Models Overview',className="graph-title"),], className="transparent-box"
    ),
    html.Br(),
    dcc.Dropdown(
        options=[
            {'label': 'RFR', 'value': 'rfr'},
            {'label': 'Varima', 'value': 'var'},
            {'label': 'DCRNN', 'value': 'DCRNN'}
        ],
        value='rfr',
        id="model-dropdown",
        className="drop-down-benshmark",
        
    ),
    
    dbc.Card(card_content, color="#A0C49D", inverse=True, style={'margin-top': '15px', 'margin-bottom': '20px'}),
            html.Br(),
            html.Div([html.H6('Error Metric Comparison',className="graph-title"),], className="transparent-box"
    ),
            html.Br(),
    dbc.Row([
            
            dbc.Col([
            html.H4('Select a Metric',className="navigation-list-new"),
            dcc.Dropdown(
                options=[
                    {'label': 'RMSE', 'value': 'RMSE'},
                    {'label': 'MSE', 'value': 'MSE'},
                    {'label': 'MAE', 'value': 'MAE'}
                ],
                value='MAE',
                id='metric-dropdown',
                className="drop-down-benshmark"
            ),],width=4),
            
            dbc.Col([html.H4('Select a Dataset',className="navigation-list-new"),
            dcc.Dropdown(
                options=[
                    {'label': 'Metr-La', 'value': 'metr_comp'},
                    {'label': 'Pems-Bay', 'value': 'bay_comp'}
                ],
                value='metr_comp',
                id='dataset-dropdown',
                className="drop-down-benshmark"
            )],width=4),
            
            dbc.Col([html.H4('Select Forecast Time',className="navigation-list-new"),
            dcc.Dropdown(
                options=[
                    {'label': '10', 'value': 'SVARMAX_10'},
                    {'label': '30', 'value': 'SVARMAX_30'},
                    {'label': '60', 'value': 'SVARMAX_60'}
                ],
                value='SVARMAX_60',
                id='forcast-dropdown',
                className="drop-down-benshmark"
            )],width=4)
            
            ]),
            html.Br(),   
            dcc.Graph(id='bar-graph',figure=defult_graph(metr_comp),className="graph-benchmark"),
             html.Br(),
            html.Br(),

            html.Div([html.H6('Models Performance',className="graph-title"),], className="transparent-box"
    ),
            html.Br(),
            dbc.Row([dbc.Col(
                [   html.H4('Select a Factor', style={'margin-top': '10px'}),
                    dcc.Dropdown(
                options=[
                    {'label': 'Inference time', 'value': 'time'},
                    {'label': 'Size', 'value': 'size'}
                ],
                value='size',
                id='factor-dropdown',
                className="drop-down-benshmark"
                    )],width=6),
            dbc.Col([
                html.H4('Select a Dataset', style={'margin-top': '10px'}),
                     
                dcc.Dropdown(
                options=[
                    {'label': 'metra', 'value': 'metr_comp'},
                    {'label': 'bay', 'value': 'bay_comp'}
                ],
                value='metr_comp',
                id='data-dropdown',
                className="drop-down-benshmark"
            )],width=6)]),
            
            html.Br(),
            dcc.Graph(id="bar-graph2",figure=size_inferance(),className="graph-benchmark"),
                ])

# Callback to update the card content
@app.callback(
    [Output("card-title", "children"), Output("card-text", "children")],
    [Input("model-dropdown", "value")]
)
def update_card_content(value):
    if value == "rfr":
        title = "Random forest regressor"
        text = "The system employs multiple models for each sensor, with each model having multiple outputs for forecasting at 10, 30, and 60-minute intervals. These models are compressed using the joblib library with a compression level of 6."
        print('rfr')
    elif value == "var":
        title = "SVarimax"
        text = "he system employs a separate model for each sensor, with each model having multiple outputs for forecasting at 10, 30, and 60-minute intervals. These models are compressed using the joblib library with a compression level of 6, which helps to reduce the amount of storage space required to store the models and allows for faster model loading times."
        print('var')
    elif value=="DCRNN":
        title = "DCRNN"
        text = "This is the card content for DCRNN"
        print('DCRNN')

    return title, text

@app.callback(
    Output('bar-graph', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('dataset-dropdown', 'value')
     ,Input('forcast-dropdown','value')])

def update_graph(metric, dataset,forcast):
    if dataset=='metr_comp':
        
        return Benchmark(metr_comp,metric,forcast)
        
    elif dataset== "bay_comp":

        return Benchmark(bay_comp,metric,forcast)
    else:
        return Benchmark(bay_comp,metric,forcast)

@app.callback(
    Output('bar-graph2', 'figure'),
    [Input('factor-dropdown', 'value'),Input('data-dropdown', 'value')]
)
def update_graph(factor,data):
    print(data,factor)
    fig_bar=size_inferance(factor,data)
    return fig_bar
