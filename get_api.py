from datetime import datetime
import time
from tqdm import tqdm
import requests

file_path_hist = 'file.txt'
file_path_hour = 'hour.txt'
file_path_minute = 'minute.txt'
file_path_btn = 'button.txt'
sensor_list='sensor.txt'
file_paths = [file_path_minute, file_path_hour, file_path_hist,file_path_btn,sensor_list]


def read_multiple_file(file_paths):
    date = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
        date.append(content)
    return date[0].strip().split(','), date[1].strip().split(','), date[2].strip().split(','),date[3].strip().split(','),date[4].strip().split(',')

def get_ui(minutes,hour,year):
    concated_date = f'{year} {hour}:{minutes}'
    timestamp = datetime.strptime(concated_date, "%Y-%m-%d %H:%M")
  
      
    # print(timestamp)
    # print(time_to_forecast)
    # print(f_sensor)
    return timestamp

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
def animation(time,num):
    if time==":"or time==None:
        return fraction_to_minutes_seconds(num)
    else:
        return ":"


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
def metr_call():
    locations = [go.Scattermapbox(
        lon=sensors_loc_data_metr['longitude'],
        lat=sensors_loc_data_metr['latitude'],
        mode='markers',
        # marker={'color': sensors_loc_data_metr['color']},
        text=sensors_loc_data_metr['sensor_id'],
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.75, 'size': 25, 'color': 'darkslategray'}},
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
  
# print(timestamp)
# lst_sensor,pred_time,true_time,pred_speed,true_speed= get_data()
