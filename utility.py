import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from tqdm import tqdm
import requests

import numpy as np

lat = 34.1522
lon = -118.2437

sensors_loc_metr= r'./dataset/graph_sensor_locations.csv'
sensors_loc_pems= r'./dataset/graph_sensor_locations_bay.csv'

metra_comp=pd.read_csv(r'./dataset/bay_comp.csv')
bay_comp=pd.read_csv(r'./dataset/metra_comp.csv') #to be as the same as the benshmark section

sensors_loc_data_pems=pd.read_csv(sensors_loc_pems)
sensors_loc_data_metr=pd.read_csv(sensors_loc_metr)

def create_sorted_bar_plot():
    data = {
        'Unnamed: 0': ['MAE', 'MSE', 'RMSE'],
        'RFR_10': [2.522100, 19.264054, 4.232973],
        'RFR_30': [3.348108, 35.133142, 5.647645],
        'RFR_60': [4.059060, 49.549950, 6.653012],
        'SVARMAX_10': [2.359731, 14.727257, 3.734769],
        'SVARMAX_30': [2.983736, 21.692871, 4.516955],
        'SVARMAX_60': [3.813687, 32.833897, 5.543247]
    }

    df = pd.DataFrame(data)

    df_melted = pd.melt(df, id_vars='Unnamed: 0', var_name='Model', value_name='Value')

    # Sort the DataFrame by the 'Value' column in ascending order
    df_melted_sorted = df_melted.sort_values('Value', ascending=True)

    # Define a homogeneous color palette for the models
    color_palette = ['#00A7E2', '#808080', '#000000']

    fig_bar = px.bar(df_melted_sorted, x='Unnamed: 0', y='Value', color='Model', barmode='group',
                     color_discrete_sequence=color_palette)

    fig_bar.update_layout(
        # title='Bar Plot',
        xaxis_title='Metrics',
        yaxis_title='ERROR',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig_bar

def Benchmark(df, metric=None,forcast_time='SVARMAX_60'):
    
    min_10_list=['Unnamed: 0','RFR_10','SVARMAX_10']
    min_30_list=['Unnamed: 0','RFR_30','SVARMAX_30']
    min_60_list=['Unnamed: 0','RFR_60','SVARMAX_60']
    if forcast_time=='SVARMAX_10':
        df=df[min_10_list]
    elif forcast_time=='SVARMAX_30':
        df=df[min_30_list]
    elif forcast_time=='SVARMAX_60':  #60 min
        df=df[min_60_list] 
          
    if metric==None:
        df_filtered=df
        # Filter the DataFrame based on the specified metric
    else :
        df_filtered = df[df['Unnamed: 0'] == metric]

    df_melted = pd.melt(df_filtered, id_vars='Unnamed: 0', var_name='Model', value_name='Value')

    # Sort the DataFrame by the 'Value' column in ascending order
    df_melted_sorted = df_melted.sort_values('Value', ascending=True)

    # Define a homogeneous color palette for the models
    #color_palette = ['#00A7E2', '#808080', '#000000']
    # modle_nme=['RFR_10','RFR_30','RFR_60','SVARMAX_10','SVARMAX_30','SVARMAX_60']
    wide=df_melted_sorted.shape[1]
    fig_bar = px.bar(df_melted_sorted, y='Unnamed: 0', x='Value', color='Model',barmode='group')
    fig_bar.update_traces( width=0.1,)

                    #  color_discrete_sequence=color_palette)

    fig_bar.update_layout(
        # title='Bar Plot',
        xaxis_title='Metrics',
        yaxis_title='ERROR',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig_bar



def defult_graph(df):
        
    
    # Filter the DataFrame based on the specified metric
    
    df_filtered = df
    
    df_melted = pd.melt(df_filtered, id_vars='Unnamed: 0', var_name='Model', value_name='Value')

    # Sort the DataFrame by the 'Value' column in ascending order
    df_melted_sorted = df_melted.sort_values('Value', ascending=True)

    # Define a homogeneous color palette for the models
    #color_palette = ['#00A7E2', '#808080', '#000000']
    
    fig_bar = px.bar(df_melted_sorted, x='Unnamed: 0', y='Value', color='Model', barmode='group')
                    #  color_discrete_sequence=color_palette)

    fig_bar.update_layout(
        # title='Bar Plot',
        xaxis_title='Metrics',
        yaxis_title='ERROR',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig_bar
    
    
    
data = {
    'Unnamed: 0': ['MAE', 'MSE', 'RMSE'],
    'RFR_10': [2.522100, 19.264054, 4.232973],
    'RFR_30': [3.348108, 35.133142, 5.647645],
    'RFR_60': [4.059060, 49.549950, 6.653012],
    'SVARMAX_10': [2.359731, 14.727257, 3.734769],
    'SVARMAX_30': [2.983736, 21.692871, 4.516955],
    'SVARMAX_60': [3.813687, 32.833897, 5.543247]
}

df = pd.DataFrame(data)


df_melted = pd.melt(df, id_vars='Unnamed: 0', var_name='Model', value_name='Value')

fig_bar = px.bar(df_melted, x='Unnamed: 0', y='Value', color='Model', barmode='group')


fig_bar.update_layout(
    title='Bar Plot',
    xaxis_title='Metrics',
    yaxis_title='Error',
    plot_bgcolor='#A0C49D',
    paper_bgcolor='#A0C49D'
)
def plot_map(df):
    # sensor_loc = pd.read_csv(path)
    sensor_loc=df.copy(deep=True)
    fig = go.Figure(data=go.Scattermapbox(
    lat=sensor_loc['latitude'],
    lon=sensor_loc['longitude'],
    mode='markers',
    # fillcolor="aliceblue",
    marker={'color' :df['color']},
    #marker=dict(color= '#d40b0b',size=10),
    unselected={'marker' : {'opacity':1}},
    selected={'marker' : {'opacity':0.75, 'size':25,'color': 'darkslategray'}},
    text=sensor_loc['sensor_id']
    ))
    
    # Set the mapbox layout
    fig.update_layout(mapbox=dict(style="open-street-map",
                                  center=dict(lat=lat, lon=lon), zoom=10))

    # Enable point selection
    fig.update_layout(uirevision= 'foo',clickmode='event+select')
    fig.update_layout(mapbox=dict(center=dict(lat=lat, lon=lon)))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    return fig

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


def fraction_to_minutes_seconds(fraction_number):
    """
    Convert a fraction number to minutes:seconds.

    Args:
        fraction_number (float): Fraction number representing the duration.

    Returns:
        str: Duration in minutes:seconds format.
    """
    minutes = int(fraction_number)
    seconds = int((fraction_number - minutes) * 60)
    return f"{minutes:02d} M : {seconds:02d} S"


def get_ui(minutes,hour,year):
    concated_date = f'{year} {hour}:{minutes}'
    timestamp = datetime.strptime(concated_date, "%Y-%m-%d %H:%M")
def get_data(sn1, sn2, date, duration):
    # API endpoint URL
    url = f"http://127.0.0.1:8000/api/sensors/{sn1}/{sn2}/{date}/{duration}/"

    # Send GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200 indicates success)
    if response.status_code == 200:
        # Access the JSON data from the response
        json_data = response.json()

        # Process the JSON data as needed
        # For example, print the data or access specific values
        print(f"{response.status_code}.....Done!!")
        loding=False
        # return json_data["nodes"],json_data["pred_time"],json_data["ture_time"],json_data["pred_speed"],json_data["true_speed"]
        return json_data,loding
    else:
        # Request was not successful, handle the error
        print("Request failed with status code:", response.status_code)
        loding=True
        return response.status_code,loding


def size_inferance(factor='time',data="metr_comp"):   
    if factor == 'time'and data=="metr_comp":
        data = {
            'factor': ['Inference time'],
            'RFR_metra': [16],
            'varmax_metra': [16],
           
             }
        df = pd.DataFrame(data)     
        df_melted = pd.melt(df, id_vars='factor', var_name='Model', value_name='Value')

        fig_bar = px.bar(df_melted, y='factor', x='Value', color='Model', barmode='group')

        fig_bar.update_layout(
            title='Bar Plot',
            xaxis_title='Time',
            yaxis_title='Time in seconds',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_bar.update_traces( width=0.1,)
        return fig_bar
    elif factor == 'size' and data== 'metr_comp':
        data = {
            'time': ['Size'],
            'RFR_metr': [193],
            'varmax_metr': [985.6]
        }
         
        df = pd.DataFrame(data)
        df_melted = pd.melt(df, id_vars='time', var_name='Model', value_name='Value')
        fig_bar = px.bar(df_melted, y='time', x='Value', color='Model', barmode='group')
        fig_bar.update_layout(
            title='Bar Plot',
            xaxis_title='Size',
            yaxis_title='size in MB',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_bar.update_traces( width=0.1,)
        return fig_bar  
    
    if factor == 'time'and data=="bay_comp":
        data = {
            'factor': ['Inference time'],
            'RFR_pems': [12],
            'varmax_pems': [480]
        }
        df = pd.DataFrame(data)     
        df_melted = pd.melt(df, id_vars='factor', var_name='Model', value_name='Value')

        fig_bar = px.bar(df_melted, y='factor', x='Value', color='Model', barmode='group')

        fig_bar.update_layout(
            title='Bar Plot',
            xaxis_title='Time',
            yaxis_title='Time in seconds',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_bar.update_traces( width=0.1,)
        return fig_bar
    elif factor == 'size' and data== 'bay_comp':
        data = {
            'time': ['Size'],
            'RFR_pems': [1331.2],
            'VARMAX_pems': [34816]
        }
        
        df = pd.DataFrame(data)
        df_melted = pd.melt(df, id_vars='time', var_name='Model', value_name='Value')

        fig_bar = px.bar(df_melted, y='time', x='Value', color='Model', barmode='group')
        fig_bar.update_traces( width=0.1,)
        fig_bar.update_layout(
        title='Bar Plot',
        xaxis_title='Size',
        yaxis_title='size in MB',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig_bar
    

def Forcast_Benshmark(df, forecast_time='SVARMAX_60'):
    df_filtered = df.loc[:, forecast_time]
    df_melted = pd.melt(df_filtered, id_vars='Unnamed: 0', var_name='Model', value_name='Value')

    # Sort the DataFrame by the 'Value' column in ascending order
    df_melted_sorted = df_melted.sort_values('Value', ascending=True)

    fig_bubble = px.scatter(df_melted_sorted, x='Unnamed: 0', y='Value', color='Model',
                            size='Value', size_max=30)

    fig_bubble.update_layout(
        xaxis_title='Metrics',
        yaxis_title='ERROR',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig_bubble