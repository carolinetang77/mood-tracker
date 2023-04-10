# Mood tracker app using Plotly Dash
# Author: carolinetang77

import os
import plotly.graph_objects as go
import math
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
            html.Div("Mood: None Energy: None", id='numeric_mood'),
            html.Div("Selected mood:"),
            html.Div("", id='text_mood'),
            dbc.Button(
                "Track mood",
                id="track-button",
                color="info",
                size="sm"
            )
            # dash_table.DataTable(
            #     id='table', 
            #     columns=[{"name": col.title(), "id": col}],
            #     sort_action="native",
            #     page_size=15,
            #     fixed_rows={'headers': True},
            #     style_cell={'textAlign': 'left'}
            # )
        ], width=6)
    ])
])

@app.callback(
    Output('numeric_mood', 'children'),
    # Output('text_mood', 'children'),
    Input('mood', 'selectedData')
)
def update_numeric_mood(selected):
    x = None
    y = None
    # text = "Please select one or more locations on the graph."
    if selected:
        x = [i['x'] for i in selected['points']]
        y = [i['y'] for i in selected['points']]
        # text = [graph_vars.graph_text[6 * math.floor(x[i]) + math.floor(y[i])] for i in range(len(x))]
    return f"Mood: {x} Energy: {y}"

@app.callback(
    Output('text_mood', 'children'),
    Input('track-button', 'n_clicks'),
    State('mood', 'selectedData')
)
def update_text_mood(n, selected):
    text = "Please select one or more locations on the graph."
    if selected:
        x = [i['x'] for i in selected['points']]
        y = [i['y'] for i in selected['points']]
        text = [graph_vars.graph_text[6 * math.floor(x[i]) + math.floor(y[i])] for i in range(len(x))]
    return f"{text}"

if __name__ == '__main__':
    app.run_server(debug=True)

