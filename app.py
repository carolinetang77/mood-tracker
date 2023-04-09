# Mood tracker app using Plotly Dash
# Author: carolinetang77

import os
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash, dcc, dash_table, html, Input, Output, State
from dash_bootstrap_templates import load_figure_template
import graph_vars

# actual app
app = dash.Dash(__name__)
server = app.server

app.layout = dbc.Container([
    html.H1('This mood tracker will eventually go kinda hard'),
    html.Br(),
    dcc.Graph(
        id = 'mood', 
        figure = graph_vars.fig,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

