import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pickle


# Creating the app
model_app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = model_app.server

with open('xgb_model.pickle', 'rb') as file:
    model = pickle.load(file=file)

years = [i for i in range(2005,2031,1)]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "32rem",
    "padding": "3rem 1rem",
    "background-color": "#c2c2c2",
}

# Content style on the right
CONTENT_STYLE = {
    "margin-left": "36rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2('Model Attributes'),
        html.Hr(),
        html.P(),
        
        # Options
        html.Div(children=[
            html.Div(children=[
                html.H4('Choose Country:'),
                dcc.Dropdown(id = 'country',
                             options=[{'label':'Kenya', 'value':'Kenya'},
                                     {'label':'Rwanda', 'value':'Rwanda'},
                                     {'label':'Ghana', 'value':'Ghana'}
                                     ],
                            placeholder='Choose Country')
            ]),
            
            # Choose Region
            html.Div(children=[
                html.H4('Choose Region:'),
                dcc.Dropdown(id='region',
                            options=[
                                {'label':'National', 'value':'National'},
                                {'label':'Urban', 'value':'Urban'},
                                {'label':'Rural', 'value':'Rural'}
                            ],
                            placeholder= 'Choose Region')
            
            ]),

            # Choose Economic Activity
            html.Div(children=[
                html.H4('Choose Economic Activity:'),
                dcc.Dropdown(id='activity',
                            options=[
                                {'label':'Total', 'value':'Total'},
                                {'label':'Agriculture', 'value':'Agriculture'},
                                {'label':'Industry', 'value':'Industry'},
                                {'label':'Services', 'value':'Services'}
                            ],
                            placeholder='Choose Economic Activity')
            ]),

            # Choose Gender
            html.Div(children=[
                html.H4('Choose Gender:'),
                dcc.Dropdown(id='gender',
                            options=[
                                {'label':'Total', 'value':'T'},
                                {'label':'Female', 'value':'F'},
                                {'label':'Male', 'value':'M'}
                            ],
                            placeholder='Choose Gender')
            ]),
            
            # Choose Year
            html.Div(children=[
                html.H4('Choose Year:'),
                dcc.Dropdown(id='year',
                            options=[
                                {'label': i, 'value': i} for i in years
                            ],
                            placeholder='Choose Year')
            ]),
        ]),
           
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(children=[
    # Dashboard title
    html.Div(html.H2('Observed Value Prediction', style={'textAlign':'center'})),
    html.Hr(), 
    # Prediction
    html.Div(children=[
        html.Div(html.H1(id='prediction', style={'textAlign':'center'}))
    ])

], style=CONTENT_STYLE)

# Creating app Layout
model_app.layout = html.Div(children=[sidebar, content])

# App Callback
@model_app.callback(Output(component_id='prediction', component_property='children'),
              
                 [Input(component_id='country', component_property='value'),
                 Input(component_id='region', component_property='value'),
                 Input(component_id='activity', component_property='value'),
                 Input(component_id='gender', component_property='value'),
                 Input(component_id='year', component_property='value')])

def get_prediction(country, region, activity, gender, year):
    
    if country is None or region is None or activity is None or gender is None or year is None:
        
        raise PreventUpdate
        
    else:
        values = {'country':country, 
                  'sex':gender, 
                  'year':year, 
                  'region':region, 
                  'activity':activity}

        df_pred = pd.DataFrame(values, index=[0])
        prediction = model.predict(df_pred)

        return prediction

# Running App
if __name__ == '__main__':
    model_app.run_server()