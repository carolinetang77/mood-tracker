# Mood tracker app using Plotly Dash
# Author: carolinetang77

import os
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash, dcc, dash_table, html, Input, Output, State
from dash_bootstrap_templates import load_figure_template
import graph_vars

fig = graph_vars.fig

# actual app
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1('This mood tracker will eventually go kinda hard'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Mood Meter'),
            dcc.Graph(
                id = 'mood', 
                figure = fig
            )
        ], width=6),
        dbc.Col([
            html.Div("Current mood: ", id='chosen_mood')
        ], width=6)
    ])
])

@app.callback(
    Output('chosen_mood', 'children'),
    Input('mood', 'selectedData')
)
def update_text(click):
    x = None
    y = None
    if click:
        x = click['points'][0]['x']
        y = click['points'][0]['y']
    return f"Mood: {round(x, 2) if x else x} Energy: {round(y, 2) if y else y}"

if __name__ == '__main__':
    app.run_server(debug=True)

