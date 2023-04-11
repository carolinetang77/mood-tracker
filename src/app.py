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
from dash import dash, dcc, dash_table, html, Input, Output, State, ctx
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
            html.H4('Mood Meter'),
            dcc.Graph(
                id = 'mood', 
                figure = fig
            )
        ], width=6),
        dbc.Col([
            html.H4("Selected mood(s)"),
            dbc.Button(
                "Track mood",
                id="track-button",
                color="info",
                size="sm"
            ),
            dash_table.DataTable(
                id='temp-table', 
                columns=[{"name": col, "id": col} for col in sorted(mood_time.keys())],
                sort_action="native",
                page_size=15,
                fixed_rows={'headers': True},
                style_cell={'textAlign': 'left'}
            ),
            html.Br(),
            html.H4("Tracked moods"),
            dbc.Button(
                "Clear cookies",
                id="clear-cookies",
                color="danger",
                size="sm"
            ),
            dash_table.DataTable(
                id='saved-table', 
                columns=[{"name": col, "id": col} for col in sorted(mood_time.keys())],
                sort_action="native",
                page_size=15,
                fixed_rows={'headers': True},
                style_cell={'textAlign': 'left'}
            )
        ], width=6)
    ])
])

# update selected table as points are chosen on the graph
@app.callback(
    Output('temp-table', 'data'),
    Input('mood', 'selectedData')
)
def update_mood_text(selected):
    x = []
    y = []
    text = []
    times = []
    if selected:
        x = [i['x'] for i in selected['points']]
        y = [i['y'] for i in selected['points']]
        text = [mood_picker.graph_text[6 * math.floor(x[i]) + math.floor(y[i])].replace('<br>', " ") for i in range(len(x))]
        times.append(dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    temp_moods = pd.DataFrame({
        'Datetime': times * len(x),
        'Mood': x,
        'Energy': y,
        'Vibe': text
    })
    return temp_moods.to_dict('records')

# update the saved data table if the track button is clicked
# delete cookies if that button is clicked (is there a way to split these up)
@app.callback(
    Output('saved-table', 'data'),
    Output('mood', 'selectedData'),
    Output('mood', 'figure'),
    Input('track-button', 'n_clicks'),
    Input('clear-cookies', 'n_clicks'),
    State('temp-table', 'data'),
    State('saved-table', 'data'),
)
def update_mood_table(n_1, n_2, selected, moods):
    button_clicked = ctx.triggered_id
    if button_clicked == "clear-cookies":
        all_cookies = dict(flask.request.cookies)
        if 'mood-tracker-cookie' in all_cookies:
            ctx.response.delete_cookie('mood-tracker-cookie')
            moods = mood_time
    else:
        if not moods:
            all_cookies = dict(flask.request.cookies)
            if 'mood-tracker-cookie' in all_cookies and all_cookies['mood-tracker-cookie'] is not None:
                moods = pd.DataFrame(eval(json.loads(all_cookies['mood-tracker-cookie'])))
            else:
                moods = mood_time
        else:
            moods = pd.DataFrame(moods)
        if selected:
            moods = pd.concat((
                pd.DataFrame(moods),
                pd.DataFrame(selected)
            ), ignore_index=True)
        ctx.response.set_cookie('mood-tracker-cookie', json.dumps(moods.to_json(orient='records')))
    return moods.to_dict('records'), None, fig.update_traces(selectedpoints=[])

if __name__ == '__main__':
    app.run_server(debug=True)

