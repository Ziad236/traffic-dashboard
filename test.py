import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State


app = dash.Dash(__name__)

global_var = 1  # Declare the global variable

# Create the layout of the application
app.layout = html.Div([
    html.Button('Update VAT', id='update-vat-button'),
    html.Div(id='vat-output'),
    html.Div(id='vat-2',children=[f"gggggggg {global_var}"]),
])

# Callback function to update and access the global_var variable
@app.callback(Output('vat-output', 'children'),
              [Input('update-vat-button', 'n_clicks')],
              [State('vat-output', 'children')])
def update_and_access_vat(n_clicks, current_vat):
    global global_var
    if n_clicks is not None:
        return f'rtreved VAT: {global_var}'
@app.callback(Output('vat-2', 'children'),
              [Input('update-vat-button', 'n_clicks')],
              [State('vat-2', 'children')])

def update_and_access_vat(n_clicks, current_vat):
    global global_var
    global_var=global_var+1
    if n_clicks is not None:
        return f'inc VAT: {global_var}'
    else:
        return f'VAT: {0}'

if __name__ == '__main__':
    app.run_server(debug=True)
