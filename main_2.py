import dash
import pandas as pd
import plotly.express as px
from dash import html,dcc
from datetime import date
import plotly.graph_objects as go
from dash import html
import dash_bootstrap_components as dbc
from dash import Dash, html, dash_table, Output, Input
from app_zid import app

from  utility import (plot_map,fig_bar,create_sorted_bar_plot
                        ,create_fig_option1,create_fig_option2,fraction_to_minutes_seconds,get_data,get_ui)
 
 
path=r"graph_sensor_locations.csv"
df = pd.read_csv(path)
df['color']= '#d40b0b'
# nodes=[]
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
sn1="--"
sn2="--"
counter=0
ls = []
hist=[]
hours=[]
minutes=[]
btn=[]
ls_show=[]

hours_options = [{'label': str(i).zfill(2), 'value': i} for i in range(24)] 


sensors_loc_metr= r'./dataset/graph_sensor_locations.csv'
sensors_loc_pems= r'./dataset/graph_sensor_locations_bay.csv'

metra_comp=pd.read_csv(r'./dataset/bay_comp.csv')
bay_comp=pd.read_csv(r'./dataset/metra_comp.csv') #to be as the same as the benshmark section

sensors_loc_data_pems=pd.read_csv(sensors_loc_pems)
sensors_loc_data_metr=pd.read_csv(sensors_loc_metr)
sensors_loc_data_metr['color']= '#d40b0b'
sensors_loc_data_pems['color']= '#d40b0b'
fig3 =  go.Figure(go.Indicator(
    gauge={'axis': {'range': [0, 120]}},
    mode = "gauge+number",
    value = 1,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Real Speed",'font': {'family': 'Arial', 'size': 36, 'color': '#15133C'}}))
# fig3.update_traces(opacity=0.7)  # Adjust the opacity value as desired (between 0 and 1)

fig3.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)'  # Set paper background color to transparent
)
fig33 =  go.Figure(go.Indicator(
    gauge={'axis': {'range': [0, 120]}},
    mode = "gauge+number",
    value = 0,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Predicted Speed",'font': {'family': 'Arial', 'size': 36, 'color': '#15133C'}}))
fig33.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
    paper_bgcolor='rgba(0,0,0,0)'  # Set paper background color to transparent
)
# fig33.update_traces(bgcolor='rgba(160, 196, 157, 0.5)')
 
# app = dash.Dash(__name__, external_stylesheets=["/assets/css/bootstrap.min.css"],prevent_initial_callbacks=True)


#app.layout
home=dbc.Container(
    [
        dbc.Row(
            [
            html.H2("Traffic Flow Forecast",className="header-traffic") 
            ]  ),
        
        
        dbc.Row([
            dbc.Col(
                    [   
                    html.H5("Select the Dataset"),
                 
                    dbc.CardBody([ 
                                dcc.Dropdown(options=[
                                {'label': 'Metr-la', 'value': 'metr'},
                                {'label': 'Pems-bay', 'value': 'pems'},

                            ],
                            value='metr', id='demo-dropdown1',className='') 
                                 ])
                    
                    ],class_name="", width=2),
            dbc.Col(
                    [   
                    html.H5("Select the Model"),
                    dcc.Dropdown([ 'Random Forest Reressor',
                                    'Varima','DCCN'], 'Varima', id='demo-dropdown2',
                                    style={'width':'100%'})
                    ],class_name="",



                width=2),
            dbc.Col([
                    # data picker selection
                    html.H5("Select the Date"),
                    dcc.DatePickerSingle(
                    id="date_picker",
                    min_date_allowed=date(2012, 6, 5),
                    max_date_allowed=date(2012, 6, 30),
                    initial_visible_month=date(2012, 6, 5),
                    display_format="MMMM D, YYYY",style={'width':'100%'})
                    ],class_name="",width=2),
            dbc.Col(    
                    [   
                        #drop down hours
                    html.H5("Select the Hour"), 
                    dcc.Dropdown([ '1','2','3','4','5','6','7','8','9','10','11','12'],
                                 '1', id='demo-dropdown5')
                    ],class_name="",

                width=2),
            dbc.Col(
                    [   
                     #drop down miniuts
                     html.H5("Select the Minute"),
                        dcc.Dropdown([ '00','05','10','15','20','25','30','35','40','45','50','55'],
                                     '00', id='demo-dropdown6',
                                    )
                    ],class_name="",

                width=2),
            dbc.Col(
                    [  
                        #dropdown forcasttime
                        html.H5("Forecast Time"),
                        dcc.Dropdown(
                                    options=[
                                            {'label': '10', 'value': 10},
                                            {'label': '30', 'value': 30},
                                            {'label': '60', 'value': 60}
                                        ],
                                        value=10,
                                        id='demo-dropdown7'
                                    )

                    ],class_name="",

                width=2)
            
             
     ]  ,className="center-row"),#row
        
        
       #map         
       dbc.Row([
                html.P(),
                dbc.Col([dbc.CardBody(dcc.Graph(id='map',figure=create_fig_option1()))],width=12)             

               ]) ,

         dbc.Row([
            html.P(),
            html.H2("Choosen Parameter",className="chossen-parameter-header"),
            #table response of the item
            dbc.Col([
                    html.H5("first_sensor",className="chossen-parameter"),
                    html.H2(id="first_sensor",children=[f"--"],className="chossen-parameter")],class_name="graph-row-card"),
            dbc.Col([
                    html.H5("second_sensor",className="chossen-parameter"),
                    html.H2(id="second_sensor",children=[f"--"],className="chossen-parameter")],class_name="graph-row-card"),
            
            dbc.Col([
                    html.H5("DataSet",className="chossen-parameter"),
                    html.H2(id="DataSet",children=[f"--"],className="chossen-parameter")],class_name="graph-row-card"),
            
            dbc.Col([
                    html.H5("Model",className="chossen-parameter"),
                    html.H2(id="Model",children=[f"--"],className="chossen-parameter")],class_name="graph-row-card"),
             dbc.Col([
                    html.H5("date",className="chossen-parameter"),
                    html.H2(id="date",children=[f"--"],className="chossen-parameter-date")],class_name="graph-row-card"),
            dbc.Col([
                    html.H5("hour",className="chossen-parameter"),
                    html.H2(id="hour",children=[f"--"],className="chossen-parameter")],class_name="graph-row-card"),
            dbc.Col([
                    html.H5("Minute",className="chossen-parameter"),
                    html.H2(id="minute",children=[f"--"],className="chossen-parameter")],class_name="graph-row-card"),
            
            dbc.Col([
                    html.H5("forecast time",className="chossen-parameter"),
                    html.H2(id="forecast_time",children=[f"--"],className="chossen-parameter")],class_name="graph-row-card"),
                ]),
       # pridiction Buttun
        dbc.Row([    
                html.P(),
                dbc.Col([dbc.Button(id="btn",n_clicks=0,children=["FORECAST"], className="prediction-button")])
                

               ]),
       
        dbc.Row([
            dbc.Col([
                #graph1
                dcc.Interval(id='interval1', interval=1000, n_intervals=0),
                html.P(),
                dcc.Graph(  id='gag1',  figure=fig3,className="graph-speed" ),
                html.P(),
                html.H3("Real Travel Time:",className="centered-text-speed"),
                
                 dbc.Card([html.Div(
                                id='clock1',
                                children=[f"58"],
                                className="custom-text-time")
                           ],class_name="graph-row-card")
                
                ],
                    class_name="graph-row",
                    width=6),
            dbc.Col([
                #graph 2
                html.P(),
                dcc.Graph(id='gag2', figure=fig33,className="graph-speed" ),
                html.P(),
                html.H3("Predicted Time Travel:",className="centered-text-speed" ),
                
                dbc.Card([html.Div(
                                 id='clock2',
                                children=[f"--"],
                                className="custom-text-time")
                          ],class_name="graph-row-card")
                ],class_name="graph-row",
                    width=6),

        ]),
        
        
        # dbc.Row([ #Benchmark
        #     dbc.Col([
        #     html.P(),
        #     html.P(),
          
        #     html.P(),
        #     dbc.Card([ 
        #               html.H5("Benchmark",className="graph-header"),
        #               dcc.Graph(
        #                     figure=create_sorted_bar_plot(),className="graph-benchmark")
        #               ],class_name="graph-row-card")
        #   ],width=12)
        #   ]),
        # html.P(),
        html.Div(id="unoutput")
        ]) 
#callback for choosen parameter
@app.callback(
    [
        Output('DataSet', 'children'),
        Output('Model', 'children'),
        Output('hour', 'children'),
        Output('minute', 'children'),
        Output('forecast_time', 'children'),
        Output('date', 'children'),
        Output('first_sensor', 'children'),
        Output('second_sensor', 'children'),
    ],
    [
        Input('demo-dropdown1', 'value'),
        Input('demo-dropdown2', 'value'),
        Input('demo-dropdown5', 'value'),
        Input('demo-dropdown6', 'value'),
        Input('demo-dropdown7', 'value'),
        Input('date_picker', 'date'),
        Input('map', 'clickData')
    ]
)
def update_dropdown_text(dataset, model, hour, minut, forcasttime, date_value,clicked_data):
    
    global ls
    global minutes
    global hours
    global date_g
    global btn
    global sn2,sn1
    global counter
    global ls_show
    
    first_sens,second_sens="--","--"
    # print("printing ", first_sens,second_sens)
    if minut is not None:
        minutes=minut
    if hour is not None:
        hours= hour  
    print(type(forcasttime))  
    btn=forcasttime
    if date_value is not None:
        date_g=date_value    
    if clicked_data is not None:
        if  clicked_data['points'][0]['text']!=sn2:
            sensor = clicked_data['points'][0]['text']
            ls_show.append(sensor)
            if len(ls_show)==1:
                first_sens=ls_show[0]
                second_sens="--"
            elif len(ls_show)==2:
                first_sens=ls_show[0]
                second_sens=ls_show[1]
                ls_show.clear()
        else:
            first_sens=sn1
            second_sens=sn2
          
    return dataset, model, hour, minut, forcasttime, date_value, first_sens,second_sens
############################################################
#                       change the map based on the dropdown
#####################################################################
#############################################################
@app.callback(
    [Output('map', 'figure',allow_duplicate=True),
     Output("date_picker", "min_date_allowed"),
    Output("date_picker", "max_date_allowed"),
    Output("date_picker", "initial_visible_month")],
    Input('demo-dropdown1', 'value')
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

####################################################################

#######                         clock animation
####################################################################
@app.callback(
    [Output('gag1', 'figure')
     ,Output('gag2', 'figure'),
    Output('clock1', 'children')
    ,Output('clock2', 'children')],
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






#############################################################
#####                       forcast buttun
################################################
@app.callback(
    [Output('unoutput','children'),
    Output('map', 'figure',allow_duplicate=True)],
    [Input('btn', 'n_clicks'),
     Input('demo-dropdown7', 'value')]
)
def perform_prediction(n_clicked,forcast_value):
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
    
    
    if n_clicked >0:
    
        loding=True
        btn=forcast_value
        timestamp=get_ui(minutes, hours, date_g)
        json_data,loding=get_data(sn1,sn2,timestamp,btn)
        nodes=json_data["nodes"]
        nodes=[int(node)for node in nodes]
        pred_time=float(json_data["pred_time"])
        ture_time=float(json_data["ture_time"])
        pred_speed=float(json_data["pred_speed"])
        true_speed=float(json_data["true_speed"])
        if df_flag=="metr":
            df=sensors_loc_data_metr.copy(deep=True)
            df["color"]='rgba(0, 255, 0, 0)'
            df["size"]=7
            change=df[df['sensor_id'].isin(nodes)]["color"].index.tolist()
            print(change,"----------------")
            df.iloc[change,-2:-1]='red'
            df.iloc[change,-1:]=12
            print("METRA***************************")
            fig = create_fig_option1(df)     
        else:
            df=sensors_loc_data_pems.copy(deep=True)
            df["color"]='rgba(0, 255, 0, 0)'
            df["size"]=7
            change=df[df['sensor_id'].isin(nodes)]["color"].index.tolist()
            print(change,"-----------------------------------------")
            df.iloc[change,-2:-1]='red'
            df.iloc[change,-1:]=12
            fig = create_fig_option2(df)

    return forcast_value,fig
#################################################################
#3                                      callback of map***#
################################################################
#create the map 
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


# def display_click_data(clickData):
#     global sn1, sn2,df_flag
#     global ls
#     global nodes
#     print("printing nodes ",nodes)
#     if clickData is not None:
#         lat = clickData['points'][0]['lat']
#         lon = clickData['points'][0]['lon']
#         sensor = clickData['points'][0]['text']
#         ls.append(sensor)
#         if df_flag=="metr":
#             df=sensors_loc_data_metr.copy(deep=True)
#             df["color"]="green"
#             df["size"]=7
#             change=df[df['sensor_id'].isin(ls)]["color"].index.tolist()
#             df.iloc[change,-2:-1]='red'
#             df.iloc[change,-1:]=12
#             if len(nodes) >1 : #need some condition to make sure that didnot print unless its starting first and second sensor
#                 print("inside the nodes")
#                 change_road=df[df['sensor_id'].isin(nodes)]["color"].index.tolist()
#                 print("changing roads",change_road)
#                 df.iloc[change_road,-2:-1]='black'
#                 df.iloc[change_road,-1:]=20
#             fig = create_fig_option1(df)     
#         else:
#             df=sensors_loc_data_pems.copy(deep=True)
#             df["color"]="green"
#             df["size"]=7
#             change=df[df['sensor_id'].isin(ls)]["color"].index.tolist()
#             df.iloc[change,-2:-1]='red'
#             df.iloc[change,-1:]=12
#             fig = create_fig_option2(df)
              
#         # df["color"]="green"
#         # change=df[df['sensor_id'].isin(ls)]["color"].index.tolist()
#         # df.iloc[change,-1:]='red'
#         # print(df.iloc[change,:])
#     if len(ls)==1:
#         sn1=ls[0]
#     if len(ls) ==2:
#         sn2=ls[1]
#     if len(ls) > 1:
#         ls.clear()  
#     return fig 
 
 
 
#the hashed one need to leave it to make sure every thing is ok       
# @app.callback(Output('map', 'figure'),
#               [Input('map', 'clickData')])

# def update_figure(clickData):   
#     #df.loc[:10,'color']="blue"   
    
#     #00FF00
#     global df
#     global ls
#     df=df.copy(deep=True)
#     fig=plot_map(df)
#     if clickData is not None:
#         # clickData['points'][0]['marker.color']='blue'
#         sensor=int(clickData['points'][0]['text'])
#         # global ls
#         ls.append(sensor)    
#         # sensor=list(map(int, ls))
#         print("the  color of the map ",df[df['sensor_id'].isin(ls)]['color'])
#         change=df[df['sensor_id'].isin(ls)]["color"].index.tolist()     
#         df.iloc[change,-1:]="green"
#         print(" lstat",ls)
#         if len(ls)  == 4 :
#             ls.clear() 
#             df['color']="red"
        
#     # Create figure
#     return fig   
           
# if __name__ == '__main__':
#     app.run_server(debug=True,port=8009)
    
