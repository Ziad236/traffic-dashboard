import dash
from dash.dependencies import Input, Output
from get_api import *
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

nodes=[]
pred_time=0
ture_time=0
pred_speed=0
true_speed=0
str_clock1=None
str_clock2=None
loding=True
hours=None
minutes=None
date_g=None
df_flag="metr"
sn1=None
sn2=None

fig3 =  go.Figure(go.Indicator(
    gauge={'axis': {'range': [0, 120]}},
    mode = "gauge+number",
    value = 1,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Real Speed",'font': {'family': 'Arial', 'size': 36, 'color': '#15133C'}}))
fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='#A0C49D'
)
fig33 =  go.Figure(go.Indicator(
    gauge={'axis': {'range': [0, 120]}},
    mode = "gauge+number",
    value = 0,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Predicted Speed",'font': {'family': 'Arial', 'size': 36, 'color': '#15133C'}}))
fig33.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='#A0C49D'
)
# Create a Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=["/assets/css/bootstrap.min.css"],prevent_initial_callbacks=True)
sensors_loc_metr= r'./dataset/graph_sensor_locations.csv'
sensors_loc_pems= r'./dataset/graph_sensor_locations_bay.csv'
metra_comp=pd.read_csv(r'./dataset/bay_comp.csv')
bay_comp=pd.read_csv(r'./dataset/metra_comp.csv')
sensors_loc_data_pems=pd.read_csv(sensors_loc_pems)
sensors_loc_data_metr=pd.read_csv(sensors_loc_metr)
hist=[]
hours=[]
minutes=[]
btn=[]
ls=[]
hours_options = [{'label': str(i).zfill(2), 'value': i} for i in range(24)]
row = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(src="/assets/giza.png", style={'width':'40%'}, className="text-left")
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        html.H2("Traffic Flow Forecasting",
                                style={'fontSize': '3rem', 'fontWeight': 'bold', 'text-indent':'250px',"margin-left":"160px", 'color':'#15133C'})
                    ],
                    width=10
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
                min_date_allowed=date(2012, 6, 5),
                max_date_allowed=date(2012, 6, 30),
                initial_visible_month=date(2012, 6, 5),
                display_format="MM/DD/YYYY",

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
            ],width=10),

            dbc.Col([ html.Div([
    html.H4("Pick prediction time",style={"color":"#15133C","font-size":"20px"}),
    html.Button('10 Minutes', id='btn-nclicks-1',value='10', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"20px","background-color":"#A0C49D","color":"#15133C","height":"100px","width":"120px"}),
    html.Button('30 Minutes', id='btn-nclicks-2',value='30', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"20px","background-color":"#A0C49D","color":"#15133C","height":"100px","width":"120px"}),
    html.Button('1 Hour', id='btn-nclicks-3',value='60', n_clicks=0,style={"padding":"20px","margin":"15px","border-radius":"7px","fontSize":"20px","background-color":"#A0C49D","color":"#15133C","height":"100px","width":"120px"}), #FCF8E8
    html.Div(id='container-button-timestamp'),
    html.Div(id='map_output'),
])
                ],width=2)
            ],style={'padding':'20px'}),
        dbc.Col(
        [ dbc.Row([
          html.Br(),html.Br(),
          dbc.Row([dbc.Col([
              dcc.Interval(id='interval1', interval=1000, n_intervals=0),
              dcc.Graph(id='gag1',
                            figure=fig3,
                            style={'height': '500px',"margin":"15px","padding":"20px","fontSize":"20px"}
                        ),html.H3("Real Travel Time:",style={'font-size': '48px', 'text-align': 'center'}),
                        dbc.Card([
                            
                  html.Div(

                      id='clock1',
                      children=[f"-"],
                      style={'font-size': '40px', 'text-align': 'center','font-family':'Orbitron'}
                  )],style={'width':'50%',"margin-left":"185px","padding":"30px","background-color":"#A0C49D"})],width=6),
              dbc.Col([
             
                  dcc.Graph(
                  id='gag2',
                  figure=fig33,
                  style={'height': '500px', "margin": "15px", "padding": "20px", "fontSize": "20px"}
                  
              ),html.H3("Predicted Time Travel:",style={'font-size': '48px', 'text-align': 'center'}),
              dbc.Card([
html.Div(
                  id='clock2',
                  children=[f"--"],
                  style={'font-size': '40px', 'text-align': 'center','font-family':'Orbitron'})],
                  style={'width':'50%',"margin-left":"190px","padding":"30px","background-color":"#A0C49D"})
                                    ], width=6),

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




#pems map
def create_fig_option2(df=[]):
    lat = 37.3382  # Latitude of San Jose
    lon = -121.8863
    fig = go.Figure(go.Scattermapbox(
        lat=sensors_loc_data_pems['latitude'],
        lon=sensors_loc_data_pems['longitude'],
        mode='markers',
        marker=dict(color='green'),
        text=sensors_loc_data_pems['sensor_id']
    ))
    if len(df) :
        df_red=df[df["color"]=="red"]
        lat_r=df_red["latitude"].iloc[-1]
        lon_r=df_red["longitude"].iloc[-1]
        fig = go.Figure(go.Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=dict(color=df['color'],size=df["size"]),
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.75, 'size': 25, 'color': 'darkolivegreen'}},
        text=df['sensor_id']
    ))
        fig.update_layout(mapbox=dict(style="open-street-map",center=dict(lat=lat_r, lon=lon_r), zoom=10))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        return fig
    fig.update_layout(mapbox=dict(style="open-street-map", center=dict(lat=lat, lon=lon), zoom=10))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


#metr map
def create_fig_option1(df=[]):
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
    if len(df) :
        df_red=df[df["color"]=="red"]
        lat_r=df_red["latitude"].iloc[-1]
        lon_r=df_red["longitude"].iloc[-1]
        fig = go.Figure(go.Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=dict(color=df['color'],size=df['size']),
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.75, 'size': 25, 'color': 'darkolivegreen'}},
        text=df['sensor_id']
    ))
        fig.update_layout(mapbox=dict(style="open-street-map",center=dict(lat=lat_r, lon=lon_r), zoom=10))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        return fig
    fig.update_layout(mapbox=dict(style="open-street-map", center=dict(lat=lat, lon=lon), zoom=10))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig
@app.callback(
    [Output('map', 'figure',allow_duplicate=True),
     Output("date_picker", "min_date_allowed"),
    Output("date_picker", "max_date_allowed"),
    Output("date_picker", "initial_visible_month")],
    Input('demo-dropdown2', 'value')
)
def update_scattermapbox(selected_option):
    global df_flag
    df_flag=selected_option
    min_date_allowed=date(2012, 6, 6)
    max_date_allowed=date(2012, 6, 30)
    initial_visible_month=date(2012, 6, 6)
    if selected_option is None:
        fig=create_fig_option1()
        
    if selected_option == 'metr':
        fig = create_fig_option1()
        # fig= metr_call()
       # print('metr')
    elif selected_option == 'pems':
        fig = create_fig_option2()
        min_date_allowed = date(2017, 5, 26)
        max_date_allowed = date(2017, 6, 30)
        initial_visible_month = date(2017, 5, 26)
        # fig= pems_call()
       # print('pems')
    return fig, min_date_allowed, max_date_allowed, initial_visible_month





#date callback
@app.callback(
    Output("output", "children"),
    Input('date_picker', 'date')
)
def update_output(date_value):
    global date_g
    if date_value is not None:
        date_g=date_value
        

@app.callback(
    Output("res_btn", "children"),
    [Input('btn-nclicks-1', 'n_clicks'),
     Input('btn-nclicks-1', 'value')]

)
def update_output(n_clicks,btn_value):
    global nodes
    global pred_time
    global ture_time
    global pred_speed
    global true_speed
    global loding
    global btn
    global minutes
    global  date_g
    global hours
    if btn_value is not None and n_clicks>0:
        loding=True
        btn=btn_value
        timestamp=get_ui(minutes, hours, date_g)
        json_data,loding=get_data(sn1,sn2,timestamp,btn)
        nodes=json_data["nodes"]
        pred_time=float(json_data["pred_time"])
        ture_time=float(json_data["ture_time"])
        pred_speed=float(json_data["pred_speed"])
        true_speed=float(json_data["true_speed"])

        return ''
@app.callback(
    Output("res_btn2", "children"),
    [Input('btn-nclicks-2', 'n_clicks'),
     Input('btn-nclicks-2', 'value')]
)
def update_output(n_clicks,btn_value):
    global nodes
    global pred_time
    global ture_time
    global pred_speed
    global true_speed
    global loding
    global btn
    global minutes
    global  date_g
    global hours
    if btn_value is not None and n_clicks>0:
        loding=True
        btn=btn_value
        timestamp=get_ui(minutes, hours, date_g)
        json_data,loding=get_data(sn1,sn2,timestamp,btn)
        nodes=json_data["nodes"]
        pred_time=float(json_data["pred_time"])
        ture_time=float(json_data["ture_time"])
        pred_speed=float(json_data["pred_speed"])
        true_speed=float(json_data["true_speed"])

    return ''
@app.callback(
    Output("res_btn3", "children"),
    [Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-3', 'value')]

)
def update_output(n_clicks,btn_value):

    global nodes
    global pred_time
    global ture_time
    global pred_speed
    global true_speed
    global loding
    global btn
    global minutes
    global  date_g
    global hours
    if btn_value is not None and n_clicks>0:
        loding=True
        btn=btn_value
        timestamp=get_ui(minutes, hours, date_g)
        json_data,loding=get_data(sn1,sn2,timestamp,btn)
        nodes=json_data["nodes"]
        pred_time=float(json_data["pred_time"])
        ture_time=float(json_data["ture_time"])
        pred_speed=float(json_data["pred_speed"])
        true_speed=float(json_data["true_speed"])

        return ''
@app.callback(
    Output("output2", "children"),
    Input("hours_dropdown", "value")
)

def update_output(selected_hours):
    global hours
    if selected_hours is not None:
        hours= selected_hours
        
@app.callback(
    Output("output3", "children"),
    Input("minutes_dropdown", "value")
)

def update_output(selected_minutes):
    global minutes
    if selected_minutes is not None:
        minutes=selected_minutes
        
       


@app.callback(
    [Output('gag1', 'figure'),Output('gag2', 'figure'),
    Output('clock1', 'children'),Output('clock2', 'children'),],
    Input('interval1', 'n_intervals')
)
def update_gauge_chart(n):
    # Calculate the updated value based on your logic
    global str_clock1
    global str_clock2
    global pred_speed
    global true_speed
    global pred_time
    global ture_time
    global loding
    if  loding ==False:
        fig3.update_traces(value=pred_speed) # Replace with your calculation logic
        fig33.update_traces(value=true_speed)
       
    
    elif n%2 and loding ==True:
        fig3.update_traces(value=120) # Replace with your calculation logic
        fig33.update_traces(value=120)
        pred_time=0
        ture_time=0
    else:
        fig3.update_traces(value=1) # Replace with your calculation logic
        fig33.update_traces(value=1)
    if pred_time==0:
        str_clock1=fraction_to_minutes_seconds(0)
        str_clock2=fraction_to_minutes_seconds(0)
   
    elif n%2 and pred_time!=0:
        str_clock1=fraction_to_minutes_seconds(pred_time)
        str_clock2=fraction_to_minutes_seconds(ture_time)
    else:
        str_clock1=':'
        str_clock2=':'
    # Update the value in the gauge chart
    return fig3,fig33,str_clock1,str_clock2
#date_call


@app.callback(
    #dash.dependencies.Output('map_output', 'children'),
     dash.dependencies.Output('map', 'figure',allow_duplicate=True),
    [dash.dependencies.Input('map', 'clickData')]
)
def display_click_data(clickData):
    global sn1, sn2,df_flag
    if clickData is not None:
        lat = clickData['points'][0]['lat']
        lon = clickData['points'][0]['lon']
        sensor = clickData['points'][0]['text']
        ls.append(sensor)
        if df_flag=="metr":
            df=sensors_loc_data_metr.copy(deep=True)
            df["color"]="green"
            df["size"]=7
            change=df[df['sensor_id'].isin(ls)]["color"].index.tolist()
            df.iloc[change,-2:-1]='red'
            df.iloc[change,-1:]=12
            fig = create_fig_option1(df)     
        else:
            df=sensors_loc_data_pems.copy(deep=True)
            df["color"]="green"
            df["size"]=7
            change=df[df['sensor_id'].isin(ls)]["color"].index.tolist()
            df.iloc[change,-2:-1]='red'
            df.iloc[change,-1:]=12
            fig = create_fig_option2(df)
              
        # df["color"]="green"
        # change=df[df['sensor_id'].isin(ls)]["color"].index.tolist()
        # df.iloc[change,-1:]='red'
        # print(df.iloc[change,:])
    if len(ls) > 1:
            sn1=ls[0]
            sn2=ls[1]
            ls.clear()  
    return fig




app.layout = dbc.Container(
    [
        row
    ],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=False, port=8001, dev_tools_hot_reload=False)
