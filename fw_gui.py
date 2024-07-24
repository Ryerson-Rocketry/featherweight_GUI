import dash_leaflet as dl
from dash import dcc, html, Dash, ctx, State
from dash.dependencies import Input, Output
from featherweight_interface import Featherweight
#import matplotlib.pyplot as plt


fw: Featherweight
app = Dash(__name__)
refresh_rate = 1000 # ms
coords=[]
mock_temp=[]
freq = 915.8
alt=[]
time=[]
app.layout = html.Div(
    html.Div([
        dl.Map([dl.TileLayer()], zoom=10, center=[0, 0], id='map'),
        html.Button('Location', id='button', n_clicks=0, style={
                    'width': '100px', 'height': '100px', 'position': 'absolute', 'bottom': '10px', 'left': '10px', 'z-index': '999'},
                    title='Go to latest location'),     
        dcc.Interval(id='interval-component', interval=refresh_rate, n_intervals=0),
        html.Div(id="fbool",children="F",style={
            'position': 'absolute', 'bottom': '25px','right':'10px','z-index': '999'
        }),
        html.Div(id="gps-data", children="GPS Data Column", style={'background-color': 'rgba(40, 67, 135,0.6)', 'padding': '10px', 'border-radius': '5px', 'position': 'absolute', 'top': '25px','right':'20px','z-index': '999'})
        ], 
    style={'width': '100%', 'height': '98vh', 'margin': "auto", "display": "block", "position": "relative"})
)

@app.callback(Output('map', 'center'), Output('map', 'zoom'), Input('button', 'n_clicks'))
def center_map(n_clicks):
    return [[0, 0], 5] if n_clicks == 0 else [fw.last_pos(), 15] 

@app.callback(Output('fbool', 'children'), Input('interval-component', 'n_intervals'))
def update_frequency(n):
    return f"Current Frequency: {fw.freq} MHz"

@app.callback(Output("gps-data", "children"), Input('interval-component', 'n_intervals'))
def update_gps_data(n):
    if fw.freq==0:
        lat = round(mock_temp[-1][-1][0], 4)  # Round to 4 decimal places
        long = round(mock_temp[-1][-1][1], 4)  # Round to 4 decimal places
        return html.Div([
            html.Div("MOCK", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'}),
            html.Div("Current Coords", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'}),
            html.Div(f"Lat:{lat}", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'}),
            html.Div(f"Long:{long}", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'})
        ], style={'line-height': '2', 'text-align': 'center'})
    
    else:
        lat = round(coords[-1][0], 4) # Round to 4 decimal places
        long = round(coords[-1][1], 4) # Round to 4 decimal places
        return html.Div([
            html.Div("GPS DATA COLUMN", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'}),
            html.Div("Current Coords:", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'}),
            html.Div(f"Lat:{lat}", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'}),
            html.Div(f"Long:{long}", style={'color': 'white', 'text-align': 'center', 'font-family': 'Roboto'})
        ], style={'line-height': '2', 'text-align': 'center'})



@app.callback(Output('map', 'children'), Input('interval-component', 'n_intervals'),Input('fbool', 'children'))
def update_map(n,f):
    data = fw.read_gps()
    if (data!='NoneType' and print_data == True):
        fw.print_gps(data)
        if fw.freq==freq:
            coords.append(fw.pos_list[-1])
            return [dl.TileLayer(),dl.Polyline(color="#0000ff",positions=coords)]
        elif fw.freq==0:            
            mock_temp.append(fw.pos_list)
            return [dl.TileLayer(),dl.Polyline(color="#ff0000",positions=fw.pos_list)]   
        else:
            return None

if __name__ == '__main__':
    from sys import argv
    print_data = True
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

    app.run(debug=False) #debug=False enables writes to .txt file 

