from datetime import datetime

file_path_hist = 'file.txt'
file_path_hour = 'hour.txt'
file_path_minute = 'minute.txt'
file_path_btn = 'button.txt'
sensor_list='sensor.txt'
file_paths = [file_path_minute, file_path_hour, file_path_hist,file_path_btn,sensor_list]


def read_multiple_file(file_paths: list):
    date = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
        date.append(content)
    return date[0].strip().split(','), date[1].strip().split(','), date[2].strip().split(','),date[3].strip().split(','),date[4].strip().split(',')


minutes,hour,year,btn,sensor=read_multiple_file(file_paths)
if len(sensor) > 1:
    f_sensor=sensor[0]
    s_sensor=sensor[1]
else:
    f_sensor=''
    s_sensor=''

if len(hour) > 1 and len(year) > 1 and len(minutes) > 1 and len(btn) > 1 :
    time_to_forecast = btn[0]
    concated_date = f'{year[0]} {hour[0]}:{minutes[0]}'
    timestamp = datetime.strptime(concated_date, "%Y-%m-%d %H:%M")
else:
    timestamp=''
    time_to_forecast=''
# print(timestamp)
# print(time_to_forecast)
# print(f_sensor)
def get_data(sensor1,sensor2,start_time,time_to_forecast):
    #url = f'http://127.0.0.1:8000/api/sensors/{sensor1}/{sensor2}/{start_time}/{time_to_forecast}/'
    lst_sensor = ["773062", "767620", "737529"]
    pred_time = 22
    true_time = 10
    pred_speed=40
    true_speed=60
    return lst_sensor,pred_time,true_time,pred_speed,true_speed


lst_sensor,pred_time,true_time,pred_speed,true_speed= get_data(f_sensor,s_sensor,timestamp,time_to_forecast)
