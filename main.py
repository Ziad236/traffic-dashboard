import dash
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
sensors_loc= 'graph_sensor_locations.csv'
sensors_loc_data=pd.read_csv(sensors_loc)
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
                                style={'fontSize': '3rem', 'fontWeight': 'bold', 
                                       'text-indent':'200px', 'color':'#15133C'})
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
                        dcc.Dropdown([ 'Select','Metr-La','Pems-bay' ], 
                                     'Select', id='demo-dropdown1',style={'width':'80%'}
                        )
                    ],

                ),
                dbc.Col(
                    [   html.H3("Select the Model",style={"color":"#15133C"}),
                        dcc.Dropdown([ 'Select','Random Forest Reressor',
                                      'Varima','DCCN'], 'Select', id='demo-dropdown2',style={'width':'80%'})
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


        dbc.Row([dbc.Col([dbc.Card([dcc.Graph(
                            figure=graphs.fig,
                            style={'height': '500px'}
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
        [ 
         dbc.Row([
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
                        ]),




        ])]),
          dbc.Row([dcc.Graph(
                            figure=graphs.fig4,
                            style={'height': '500px',"margin":"15px","padding":"20px"}
                        )],width=12)
    ],

),

],style={"margin":"20px"})],fluid=True,
    style={'backgroundColor': '#FCF8E8'})

#F0EDD4
#EEEEEE

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