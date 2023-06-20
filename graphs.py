import pandas as pd
import dash
from dash import html,dcc
sensor_loc = pd.read_csv(r'C:\Users\Ziad\PycharmProjects\pythonProject3\graph_sensor_locations.csv')

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
    lat=sensor_loc['latitude'],
    lon=sensor_loc['longitude'],
    mode='markers',
    marker=dict(color='green'),
    text=sensor_loc['sensor_id']
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
# Show the plot
#fig.show()


df = px.data.gapminder().query("continent == 'Oceania'")
fig2 = px.line(df, x='year', y='lifeExp', color='country', symbol="country",title="Prediction result VS Ground Truth")

fig2.update_layout(
    plot_bgcolor='#A0C49D',
    paper_bgcolor='#A0C49D'
)
df = px.data.gapminder().query("continent == 'Oceania'")
fig4 = px.line(df, x='year', y='lifeExp', color='country', symbol="country",title="Random Forest Regressor VS Varima")

fig4.update_layout(
    plot_bgcolor='#A0C49D',
    paper_bgcolor='#A0C49D'
)

fig3 = go.Figure(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=45.5,
    mode="gauge+number+delta",
    title={'text': "Speed"},
    delta={'reference': 100},
    gauge={'axis': {'range': [None, 500]},
           'steps': [
               {'range': [0, 50], 'color': "lightgray"},
               {'range': [50, 100], 'color': "gray"}],
           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 1, 'value': 490}}))
fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='#A0C49D'
)






