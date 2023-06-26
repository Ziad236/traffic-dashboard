import pandas as pd
import dash
import get_api
from dash import html,dcc
from dash.dependencies import Input, Output
sensor_loc_metr = pd.read_csv(r'./dataset/graph_sensor_locations.csv')
sensor_loc_pems = pd.read_csv(r'./dataset/graph_sensor_locations_bay.csv')
metra_comp=pd.read_csv(r'./dataset/bay_comp.csv')
bay_comp=pd.read_csv(r'./dataset/metra_comp.csv')
import plotly.express as px
import plotly.graph_objects as go
lat = 34.1522
lon = -118.2437

# Create a scatter_mapbox plot with Los Angeles as the center
# fig = px.scatter_mapbox(sensor_loc, lat="latitude", lon="longitude", hover_name="sensor_id",
#                         color_discrete_sequence=["green"], zoom=10.2, height=500)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(mapbox=dict(center=dict(lat=lat, lon=lon)))
# fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

fig = go.Figure(go.Scattermapbox(
    lat=sensor_loc_pems['latitude'],
    lon=sensor_loc_pems['longitude'],
    mode='markers',
    marker=dict(color='green'),
    text=sensor_loc_pems['sensor_id']
))




# Set the mapbox layout
fig.update_layout(mapbox=dict(style="open-street-map", center=dict(lat=lat, lon=lon), zoom=10))

# Enable point selection
fig.update_layout(clickmode='event+select')
fig.update_layout(mapbox=dict(center=dict(lat=lat, lon=lon)))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
# Initialize selected points list
selected_points = []

# Define callback function for point selection
def handle_selection(trace, points, selector):
    global selected_points
    if len(selected_points) < 2:
        selected_points.extend(points.point_inds)
        selected_points.append()
        print("Selected Points:", selected_points)
    else:
        print("Maximum selection reached.")

# Register callback function for point selection event
fig.data[0].on_selection(handle_selection)
print(selected_points)



# df_metr = metra_comp
#
#
# fig2 =  go.Figure(title="Prediction result VS Ground Truth",
#     data=[
#     go.Bar(name='RFR', x=df_metr.columns, y=[, 14, 23]),
#     go.Bar(name='VARIMA', x=df_metr.columns, y=[12, 18, 29])
# ])
# # Change the bar mode
# fig.update_layout(barmode='group')
#
# fig2.update_layout(
#     plot_bgcolor='#A0C49D',
#     paper_bgcolor='#A0C49D'
# )

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
    yaxis_title='Values',
    plot_bgcolor='#A0C49D',
    paper_bgcolor='#A0C49D'
)

fig3 =  go.Figure(go.Indicator(
    gauge={'axis': {'range': [0, 120]}},
    mode = "gauge+number",
    value = 4,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Real Speed",'font': {'family': 'Arial', 'size': 36, 'color': '#15133C'}}))
fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='#A0C49D'
)
fig33 =  go.Figure(go.Indicator(
    gauge={'axis': {'range': [0, 120]}},
    mode = "gauge+number",
    value = 7,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Predicted Speed",'font': {'family': 'Arial', 'size': 36, 'color': '#15133C'}}))
fig33.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='#A0C49D'
)



def plot_map(path):
    sensor_loc = pd.read_csv(path)

    fig_map = go.Figure(data=go.Scattermapbox(
        lat=sensor_loc['latitude'],
        lon=sensor_loc['longitude'],
        mode='markers',
        fillcolor="aliceblue",
        marker={'color': 'green'},
        unselected={'marker': {'opacity': 1}},
        # selected={'marker': {'opacity': 0.75, 'size': 25, 'color': 'darkolivegreen'}},
        # marker=dict(color= '#d40b0b',size=10),

        text=sensor_loc['sensor_id']
    ))

    # Set the mapbox layout
    fig_map.update_layout(mapbox=dict(style="open-street-map",
                                  center=dict(lat=lat, lon=lon), zoom=10))

    # Enable point selection
    fig_map.update_layout(clickmode='event+select')
    fig_map.update_layout(mapbox=dict(center=dict(lat=lat, lon=lon)))
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    return fig_map


#fig.update_layout(clickmode='event+select')

file_path = 'file.txt'
def to_write(var,to_write):
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the new content
        file.write(f"{var},{to_write} ")

