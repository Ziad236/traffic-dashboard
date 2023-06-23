import dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import graphs
from dash import html,dcc
from datetime import date
import plotly.graph_objects as go
import plotly
from dash import html
import dash
import dash_bootstrap_components as dbc
# Create a Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=["/assets/css/bootstrap.min.css"])
sensors_loc_metr= r'C:\Users\Ziad\PycharmProjects\pythonProject3\dataset\graph_sensor_locations.csv'
sensors_loc_pems= r'C:\Users\Ziad\PycharmProjects\pythonProject3\dataset\graph_sensor_locations_bay.csv'
sensors_loc_data_pems=pd.read_csv(sensors_loc_pems)
sensors_loc_data_metr=pd.read_csv(sensors_loc_metr)
row = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(src="/assets/giza.png", style={'width':'250px'}, className="text-left")
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        html.H2("Traffic Forecast",
                                style={'fontSize': '3rem', 'fontWeight': 'bold', 'text-indent':'200px', 'color':'#15133C'})
                    ],
                    width=8
                ),
            ],
            align='center',
            style={'align-items': 'center'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [   html.H3("Select the Dataset",style={"color":"#15133C"}),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Metr-la', 'value': 'metr'},
                                {'label': 'Pems-bay', 'value': 'pems'},

                            ],
                            value='Select',
                            id='demo-dropdown2',
                            style={'width': '80%'}
                        ),
                    ],

                ),
                dbc.Col(
                    [   html.H3("Select the Model",style={"color":"#15133C"}),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Random Forest Regressor', 'value': 'rf'},
                                {'label': 'VARIMA', 'value': 'varima'},
                                {'label': 'DCCN', 'value': 'dccn'}
                            ],
                            value='Select',
                            id='demo-dropdown3',
                            style={'width': '80%'}
                        ),
                    ],



                ),
dbc.Col([
    dcc.DatePickerSingle(

                id="date_picker",
                min_date_allowed=date(2012, 3, 1),
                max_date_allowed=date(2012, 6, 30),
                initial_visible_month=date(2012, 3, 1),
                display_format="MMMM D, YYYY",

            ),
                 ],
            style={'width':'100%','margin':'50px'},
            className='mt-3'),
            dbc.Col(
                    [   html.H3("Select the Hour",style={"color":"#15133C"}),
                        dcc.Dropdown([ 'Select','1','2','3','4','5','6','7','8','9','10','11','12'], 'Select', id='demo-dropdown5',style={'width':'80%'})
                    ],

                ),
dbc.Col(
                    [   html.H3("Select the Minute",style={"color":"#15133C"}),
                        dcc.Dropdown([ 'Select','00','05','10','15','20','25','30','35','40','45','50','55'], 'Select', id='demo-dropdown6',style={'width':'80%'})
                    ],

                ),

#map
        dbc.Row([dbc.Col([dbc.Card([dcc.Graph(id='map',figure={},style={'height':'100%','width':'100%'}

                        )])
            ],width=11),
            dbc.Col([ html.Div([
    html.H4("Pick prediction time",style={"color":"#15133C"}),
    html.Button('10 Minutes', id='btn-nclicks-1', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"24px","background-color":"#A0C49D","color":"#15133C"}),
    html.Button('30 Minutes', id='btn-nclicks-2', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"24px","background-color":"#A0C49D","color":"#15133C"}),
    html.Button('1 Hour', id='btn-nclicks-3', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"24px","background-color":"#A0C49D","color":"#15133C"}), #FCF8E8
    html.Div(id='container-button-timestamp')
])
                ],width=1)
            ],style={'padding':'20px'}),
        dbc.Col(
        [ dbc.Row([
          html.Br(),html.Br(),
          dbc.Row([dbc.Col([dcc.Graph(
                            figure=graphs.fig2,
                            style={'height': '500px',"margin":"15px","padding":"20px","fontSize":"20px"}
                        )],width=9),
              dbc.Col([dbc.Card([dcc.Graph(
                figure=graphs.fig3,
                style={'height': '500px'}
            ),
                  ],style={'padding':'20px',"margin":"30px","background-color":"#A0C49D",'height': '465px'})
                        ],width=3),




        ])]),
          dbc.Row([dcc.Graph(
                            figure=graphs.fig4,
                            style={'height': '500px',"margin":"15px","padding":"20px"}
                        )])
    ],

),

],style={"margin":"20px"})],fluid=True,
    style={'backgroundColor': '#FCF8E8'})




#pems map
def create_fig_option2():
    lat = 37.3382  # Latitude of San Jose
    lon = -121.8863
    fig = go.Figure(go.Scattermapbox(
        lat=sensors_loc_data_pems['latitude'],
        lon=sensors_loc_data_pems['longitude'],
        mode='markers',
        marker=dict(color='green'),
        text=sensors_loc_data_pems['sensor_id']
    ))
    fig.update_layout(mapbox=dict(style="open-street-map", center=dict(lat=lat, lon=lon), zoom=10))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


#metr map
def create_fig_option1():
    lat = 34.1522
    lon = -118.2437
    fig = go.Figure(go.Scattermapbox(
        lat=sensors_loc_data_metr['latitude'],
        lon=sensors_loc_data_metr['longitude'],
        mode='markers',
        marker=dict(color='green'),
        text=sensors_loc_data_metr['sensor_id']
    ))
    fig.update_layout(mapbox=dict(style="open-street-map", center=dict(lat=lat, lon=lon), zoom=10))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig
@app.callback(
    Output('map', 'figure'),
    Input('demo-dropdown2', 'value')
)
def update_scattermapbox(selected_option):
    fig={}
    if selected_option == 'metr':
        fig = create_fig_option1()
       # print('metr')
    elif selected_option == 'pems':
        fig = create_fig_option2()
       # print('pems')
    return fig


app.layout = dbc.Container(
    [
        row
    ],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
    #plot_map(r"C:\Users\Ziad\PycharmProjects\pythonProject3\graph_sensor_locations.csv")
    #print(sensors_loc_data['latitude'].values)