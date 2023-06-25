import dash
from dash.dependencies import Input, Output
import test

import pandas as pd
from datetime import datetime
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
app = dash.Dash(__name__, external_stylesheets=["/assets/css/bootstrap.min.css"],prevent_initial_callbacks=True)
sensors_loc_metr= r'C:\Users\Ziad\PycharmProjects\pythonProject3\dataset\graph_sensor_locations.csv'
sensors_loc_pems= r'C:\Users\Ziad\PycharmProjects\pythonProject3\dataset\graph_sensor_locations_bay.csv'
metra_comp=pd.read_csv(r'C:\Users\Ziad\PycharmProjects\pythonProject3\dataset\bay_comp.csv')
bay_comp=pd.read_csv(r'C:\Users\Ziad\PycharmProjects\pythonProject3\dataset\metra_comp.csv')
sensors_loc_data_pems=pd.read_csv(sensors_loc_pems)
sensors_loc_data_metr=pd.read_csv(sensors_loc_metr)
hist=[]
hours=[]
minutes=[]
btn=[]
ls=[]
file_path='sensor.txt'
hours_options = [{'label': str(i).zfill(2), 'value': i} for i in range(24)]
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
                            value='metr',
                            id='demo-dropdown2',
                            style={'width': '80%'}
                        ),
                    ],

                ),
                # dbc.Col(
                #     [   html.H3("Select the Model",style={"color":"#15133C"}),
                #         dcc.Dropdown(
                #             options=[
                #                 {'label': 'Random Forest Regressor', 'value': 'rf'},
                #                 {'label': 'VARIMA', 'value': 'varima'},
                #                 {'label': 'DCCN', 'value': 'dccn'}
                #             ],
                #             value='Select',
                #             id='demo-dropdown3',
                #             style={'width': '80%'}
                #         ),
                #     ],
                #
                #
                #
                # ),
dbc.Col([
    html.H3("Select the Date",style={"color":"#15133C","margin-top":"-17px"}),
    dcc.DatePickerSingle(

                id="date_picker",
                min_date_allowed=date(2012, 3, 1),
                max_date_allowed=date(2012, 6, 30),
                initial_visible_month=date(2012, 3, 1),
                display_format="MMMM D, YYYY",

            ),

            html.Div(id="output")
                 ],
            style={'width':'100%','margin':'50px'},
            className='mt-3'),
            dbc.Col(
                    [   html.H3("Select the Hour",style={"color":"#15133C"}),
                        dcc.Dropdown(
                            id="hours_dropdown",
                            options=hours_options,
                            value=None,
                            style={"width":"80%"}),
                        html.Div(id="output2")

                    ],

                ),
dbc.Col(
                    [   html.H3("Select the Minute",style={"color":"#15133C"}),
                        dcc.Dropdown([ 'Select','00','05','10','15','20','25','30','35','40','45','50','55'], None, id='minutes_dropdown',style={'width':'80%'}),
                        html.Div(id="output3")
                    ],

                ),

#map
        dbc.Row([dbc.Col([dbc.Card([dcc.Graph(id='map',figure=graphs.plot_map(sensors_loc_metr),style={'height':'100%','width':'100%'}

                        )])
            ],width=11),

            dbc.Col([ html.Div([
    html.H4("Pick prediction time",style={"color":"#15133C"}),
    html.Button('10 Minutes', id='btn-nclicks-1',value='10', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"20px","background-color":"#A0C49D","color":"#15133C","height":"100px","width":"120px"}),
    html.Button('30 Minutes', id='btn-nclicks-2',value='30', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"20px","background-color":"#A0C49D","color":"#15133C","height":"100px","width":"120px"}),
    html.Button('1 Hour', id='btn-nclicks-3',value='60', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"20px","background-color":"#A0C49D","color":"#15133C","height":"100px","width":"120px"}), #FCF8E8
    html.Div(id='container-button-timestamp'),
    html.Div(id='map_output'),
])
                ],width=1)
            ],style={'padding':'20px'}),
        dbc.Col(
        [ dbc.Row([
          html.Br(),html.Br(),
          dbc.Row([dbc.Col([
              #dcc.Interval(id='interval1', interval=2000, n_intervals=0),
              dcc.Graph(id='gag1',
                            figure=graphs.fig3,
                            style={'height': '500px',"margin":"15px","padding":"20px","fontSize":"20px"}
                        ),html.H3("Real Time Travel:",style={'font-size': '48px', 'text-align': 'center'}),
              html.Div(
                  id='clock',
                  children=[test.true_time],
                  style={'font-size': '48px', 'text-align': 'center'}
              )],width=6),
              dbc.Col([

                  dcc.Graph(
                  id='gag2',
                  figure=graphs.fig33,
                  style={'height': '500px', "margin": "15px", "padding": "20px", "fontSize": "20px"}
              ),html.H3("Predicted Time:",style={'font-size': '48px', 'text-align': 'center'}),
                  html.Div(

                      id='clock1',
                      children=[test.pred_time],
                      style={'font-size': '48px', 'text-align': 'center'}
                  )], width=6),

        ])]),
          dbc.Row([dcc.Graph(
                            figure=graphs.fig_bar,
                            style={'height': '500px',"margin":"15px","padding":"20px"}
                        ),
html.Div([html.Plaintext(id='res_btn'),html.Plaintext(id='res_btn2'),html.Plaintext(id='res_btn3')]),

          ])
    ],

),

],style={"margin":"20px"})],fluid=True,
    style={'backgroundColor': '#FCF8E8'})



file_path_hist = 'file.txt'
file_path_hour = 'hour.txt'
file_path_minute = 'minute.txt'
file_path_btn = 'button.txt'
def to_write_hist(val1,val2):
    # Open the file in write mode
    with open(file_path_hist, 'a') as file:
        # Write the new content
        file.write(f"{val1},{val2}")
def to_write_hour(val1,val2):
    # Open the file in write mode
    with open(file_path_hour, 'a') as file:
        # Write the new content
        file.write(f"{val1},{val2}")
def to_write_minute(val1,val2):
    # Open the file in write mode
    with open(file_path_minute, 'a') as file:
        # Write the new content
        file.write(f"{val1},{val2}")
def to_write_btn(val1,val2):
    # Open the file in write mode
    with open(file_path_btn, 'a') as file:
        # Write the new content
        file.write(f"{val1},{val2}")
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
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.75, 'size': 25, 'color': 'darkolivegreen'}},
        text=sensors_loc_data_metr['sensor_id']
    ))
    fig.update_layout(mapbox=dict(style="open-street-map", center=dict(lat=lat, lon=lon), zoom=10))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig
@app.callback(
    Output('map', 'figure',allow_duplicate=True),
    Input('demo-dropdown2', 'value')
)
def update_scattermapbox(selected_option):
    if selected_option is None:
        fig=create_fig_option1()
    if selected_option == 'metr':
        fig = create_fig_option1()
        # fig= metr_call()
       # print('metr')
    elif selected_option == 'pems':
        fig = create_fig_option2()
        # fig= pems_call()
       # print('pems')
    return fig


def metr_call():
    locations = [go.Scattermapbox(
        lon=sensors_loc_data_metr['longitude'],
        lat=sensors_loc_data_metr['latitude'],
        mode='markers',
        # marker={'color': sensors_loc_data_metr['color']},
        text=sensors_loc_data_metr['sensor_id'],
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.75, 'size': 25, 'color': 'darkslategray'}},
        # hoverinfo=df['sensor_id'],
        #  hovertext=df['hov_txt'],
        #  customdata=df['website']
    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            # uirevision='foo',  # preserves state of figure/map after callback activated
            clickmode='event+select',
            # hovermode='closest',
            # hoverdistance=2,
            title=dict(text="How Long is it take?", font=dict(size=50, color='green')),
            mapbox=dict(
                bearing=25,
                style='light',
                center=dict(
                    lat=40.80105,
                    lon=-73.945155
                ),
                pitch=40,
                zoom=11.5
            ),
        )
    }
def pems_call():
    locations = [go.Scattermapbox(
        lon=sensors_loc_data_pems['longitude'],
        lat=sensors_loc_data_pems['latitude'],
        mode='markers',
        # marker={'color': sensors_loc_data_metr['color']},
        text=sensors_loc_data_pems['sensor_id'],
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.75, 'size': 25, 'color': 'darkslategray'}},
        # hoverinfo=df['sensor_id'],
        #  hovertext=df['hov_txt'],
        #  customdata=df['website']
    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            # uirevision='foo',  # preserves state of figure/map after callback activated
            clickmode='event+select',
            # hovermode='closest',
            # hoverdistance=2,
            title=dict(text="How Long is it take?", font=dict(size=50, color='green')),
            mapbox=dict(
                bearing=25,
                style='light',
                center=dict(
                    lon=sensors_loc_data_pems['longitude'][0],
                    lat=sensors_loc_data_pems['latitude'][0]
                ),
                pitch=40,
                zoom=11.5
            ),
        )
    }

#date callback
@app.callback(
    Output("output", "children"),
    Input('date_picker', 'date')
)
def update_output(date_value):
    if date_value is not None:
        hist.append(date_value)
        if len(hist) == 1:
            to_write_hist(hist[0],'')
        return f'selected date  =>{date_value} '
    else:
        return 'enter the date'

@app.callback(
    Output("res_btn", "children"),
    [Input('btn-nclicks-1', 'n_clicks'),
     Input('btn-nclicks-1', 'value')]

)
def update_output(n_clicks,btn_value):
    if btn_value is not None and n_clicks>0:
        btn.append(btn_value)
        to_write_btn(btn[-1],'')
       # return f'selected time  =>{btn} '
    # else:
    #     return 'enter the date'
@app.callback(
    Output("res_btn2", "children"),
    [Input('btn-nclicks-2', 'n_clicks'),
     Input('btn-nclicks-2', 'value')]
)
def update_output(n_clicks,btn_value):
    if btn_value is not None and n_clicks>0:
        btn.append(btn_value)
        to_write_btn(btn[-1],'')
        return f'selected time  =>{btn} '
    else:
        return 'enter the date'
@app.callback(
    Output("res_btn3", "children"),
    [Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-3', 'value')]

)
def update_output(n_clicks,btn_value):

    if btn_value is not None and n_clicks>0:
        btn.append(btn_value)
        to_write_btn(btn[-1],'')
        return f'selected time  =>{btn} '
    else:
        return 'enter the date'
@app.callback(
    Output("output2", "children"),
    Input("hours_dropdown", "value")
)

def update_output(selected_hours):
    if selected_hours is not None:
        hours.append(selected_hours)
        if len(hours) == 1:
            to_write_hour(hours[2],'')
        return f'selected hours  =>{hours} '
    else:
        return 'enter the date'
@app.callback(
    Output("output3", "children"),
    Input("minutes_dropdown", "value")
)

def update_output(selected_minutes):
    if selected_minutes is not None:
        minutes.append(selected_minutes)
        if len(minutes) == 1:
            to_write_minute(minutes[0], '')
        return f'selected minutes  =>{minutes} '
    else:
        return 'enter the date'


if len(hist) < 1 and len(hours) <1 and len(minutes):
    total_hist=f'{hist[0]}+{hours[0]}+{minutes[0]}'
    #print(total_hist)

#date_call
@app.callback(
    dash.dependencies.Output('clock', 'children'),
    dash.dependencies.Input('gag1', 'id')
)
def update_clock(value):
    # Get the current time
    print(value,'ajhaoihqa')
    now = test.pred_time
    return now
@app.callback(
    dash.dependencies.Output('clock1', 'children'),
    dash.dependencies.Input('gag2', 'id')
)
def update_clock(_):
    # Get the current time
    now = test.true_time

    return now

def to_write(val1,val2):
    # Open the file in write mode
    with open(file_path, 'w+') as file:
        # Write the new content
        file.write(f"{val1},{val2} ")
@app.callback(
    dash.dependencies.Output('map_output', 'children'),
    [dash.dependencies.Input('map', 'clickData')]
)
def display_click_data(clickData):
    if clickData is not None:
        lat = clickData['points'][0]['lat']
        lon = clickData['points'][0]['lon']
        sensor = clickData['points'][0]['text']
        # global ls
        ls.append(sensor)
        # f = open("file.txt","a")
        # f.write(str(sensor))
        # f.close()
        if len(ls) == 2:
            to_write(ls[0], ls[1])
    #     return f'sensor_id  =>{ls} '
    # else:
    #     return 'Click on a point to get its coordinates'


# change  color map after selecting some points
# Output of Graph
# @app.callback(Output('map', 'figure',allow_duplicate=True),
#               [Input('map', 'clickData'),
#                Input('demo-dropdown2', 'value')])
# def update_figure(clickData,value):
#     # df.loc[:10,'color']="blue"
#     # 00FF00
#     print(value)
#     if value == 'metr':
#        metr_call()
#     else:
#         return pems_call()


# @app.callback(
#     Output('gag1', 'figure'),
#     Input('interval1', 'n_intervals')
# )
# def update_gauge_chart(n):
#     # Calculate the updated value based on your logic
#
#     updated_value = test.pred_speed  # Replace with your calculation logic
#
#     # Update the value in the gauge chart
#     graphs.fig3.update_traces(values=[updated_value])
#
#     return graphs.fig3
# @app.callback(
#     Output('gag2', 'figure'),
#     Input('interval2', 'n_intervals')
# )
# def update_gauge_chart(n):
#     # Calculate the updated value based on your logic
#
#     updated_value = test.true_speed  # Replace with your calculation logic
#
#     # Update the value in the gauge chart
#     graphs.fig33.update_traces(values=[updated_value])
#
#     return graphs.fig33
file_paths=[file_path_minute,file_path_hour,file_path_hist]
def read_multiple_file(file_paths:list):
    date=[]

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            # Process the file content
            #print(content)
        date.append(content)
    return date[0].strip().split(','),date[1].strip().split(','),date[2].strip().split(',')

read_multiple_file(file_paths)



app.layout = dbc.Container(
    [
        row
    ],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
