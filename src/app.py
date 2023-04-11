# Mood tracker app using Plotly Dash
# Author: carolinetang77

import os
import plotly.graph_objects as go
import math
import datetime as dt
import pandas as pd
import flask
import json
import dash_bootstrap_components as dbc
from dash import dash, dcc, dash_table, html, Input, Output, State, callback_context
from dash_bootstrap_templates import load_figure_template
import mood_picker

fig = mood_picker.fig

mood_time = pd.DataFrame({'Datetime': [], 'Mood': [], 'Energy': [], 'Vibe': []})

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
            html.Div("Selected vibes:"),
            html.Div("", id='text_mood'),
            html.Div("Mood: None Energy: None", id='numeric_mood'),
            dbc.Button(
                "Track mood",
                id="track-button",
                color="info",
                size="sm"
            ),
            dash_table.DataTable(
                id='table', 
                columns=[{"name": col, "id": col} for col in sorted(mood_time.keys())],
                sort_action="native",
                page_size=15,
                fixed_rows={'headers': True},
                style_cell={'textAlign': 'left'}
            )
        ], width=6)
    ])
])

@app.callback(
    Output('numeric_mood', 'children'),
    Output('text_mood', 'children'),
    Input('mood', 'selectedData')
)
def update_mood_text(selected):
    x = None
    y = None
    text = """Please select one or more locations on the graph. 
    You can select multiple locations by holding down shift while clicking on the graph."""
    if selected:
        x = [i['x'] for i in selected['points']]
        y = [i['y'] for i in selected['points']]
        text = [mood_picker.graph_text[6 * math.floor(x[i]) + math.floor(y[i])].replace('<br>', " ") for i in range(len(x))]
    return f"Mood: {x} Energy: {y}", f"{text}"

@app.callback(
    Output('table', 'data'),
    Output('mood', 'selectedData'),
    Output('mood', 'figure'),
    Input('track-button', 'n_clicks'),
    State('mood', 'selectedData'),
    State('table', 'data')
)
def update_mood_table(n, selected, moods):
    if not moods:
        all_cookies = dict(flask.request.cookies)
        if 'mood-tracker-cookie' in all_cookies:
            moods = pd.DataFrame(eval(json.loads(all_cookies['mood-tracker-cookie'])))
            print(moods)
        else:
            moods = mood_time
    if selected:
        x = [i['x'] for i in selected['points']]
        y = [i['y'] for i in selected['points']]
        text = [mood_picker.graph_text[6 * math.floor(x[i]) + math.floor(y[i])].replace('<br>', " ") for i in range(len(x))]
        moods = pd.concat((
            pd.DataFrame(moods),
            pd.DataFrame({
                'Datetime': [dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')] * len(x),
                'Mood': x,
                'Energy': y,
                'Vibe': text
            })
        ), ignore_index=True)
    callback_context.response.set_cookie('mood-tracker-cookie', json.dumps(moods.to_json(orient='records')))
    return moods.to_dict('records'), None, fig.update_traces(selectedpoints=[])

if __name__ == '__main__':
    app.run_server(debug=True)

