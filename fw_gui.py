import dash_leaflet as dl
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
from featherweight_interface import Featherweight


fw: Featherweight
app = Dash(__name__)
refresh_rate = 1000 # ms

app.layout = html.Div(
    html.Div([
        dl.Map([dl.TileLayer()], zoom=10, center=[0, 0], id='map'),
        html.Button('Location', id='button', n_clicks=0, style={
                    'width': '100px', 'height': '100px', 'position': 'absolute', 'bottom': '10px', 'left': '10px', 'z-index': '999'},
                    title='Go to latest location'),
        dcc.Interval(id='interval-component', interval=refresh_rate, n_intervals=0)
        ], 
    style={'width': '100%', 'height': '98vh', 'margin': "auto", "display": "block", "position": "relative"})
)


@app.callback(Output('map', 'center'), Output('map', 'zoom'), Input('button', 'n_clicks'))
def center_map(n_clicks):
    return [[0, 0], 5] if n_clicks == 0 else [fw.last_pos(), 15]


@app.callback(Output('map', 'children'), Input('interval-component', 'n_intervals'))
def update_map(n):
    fw.read_gps()
    return [dl.TileLayer(), dl.Polyline(positions=fw.pos_list)]


if __name__ == '__main__':
    from sys import argv

    args = argv[1:]

    if args == []:
        print("Error: No command line arguments given")
        print("Usage: featherweight_interface.py <port | mock>")
        exit(1)

    try:
        fw = Featherweight(args[0])
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    app.run(debug=True)