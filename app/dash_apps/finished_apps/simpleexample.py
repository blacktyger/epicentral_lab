import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample')  # replaces dash.Dash

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

app.layout = html.Div([
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[],
        value=['slider']
        ),
    dcc.Graph(id="graph"),
    ])


@app.callback(
    Output("graph", "figure"),
    [Input("toggle-rangeslider", "value")])
def display_candlestick(value):
    fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Range Slider and Selectors')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
                ])
            )
        )
    fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_rangeslider_visible='slider' in value
        )
    return fig
# -------------------------------------------------------------------
#
#
# app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
# print(df)
#
# app.layout = html.Div([
#     dcc.Checklist(
#         id='toggle-rangeslider',
#         options=[{'label': 'Include Rangeslider',
#                   'value': 'slider'}],
#         value=['slider']
#         ),
#     dcc.Graph(id="graph"),
#     ])
#
#
# @app.callback(
#     Output("graph", "figure"),
#     [Input("toggle-rangeslider", "value")])
# def display_candlestick(value):
#     fig = go.Figure(go.Candlestick(
#         x=df['Date'],
#         open=df['AAPL.Open'],
#         high=df['AAPL.High'],
#         low=df['AAPL.Low'],
#         close=df['AAPL.Close']
#         ))
#
#     layout = go.Layout(
#         xaxis_rangeslider_visible='slider' in value,
#         paper_bgcolor='#27293d',
#         plot_bgcolor='rgba(0,0,0,0)',
#         font=dict(color='white'),
#
#         )
#     return {'data': [fig], 'layout': layout}
#

# app.layout = html.Div([
#     html.H1('Square Root Slider Graph'),
#     dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
#     dcc.Slider(
#         id='slider-updatemode',
#         marks={i: '{}'.format(i) for i in range(20)},
#         max=20,
#         value=2,
#         step=1,
#         updatemode='drag',
#         ),
#     ])
#
#
# @app.callback(
#     Output('slider-graph', 'figure'),
#     [Input('slider-updatemode', 'value')])
# def display_value(value):
#     x = []
#     for i in range(value):
#         x.append(i)
#
#     y = []
#     for i in range(value):
#         y.append(i * i)
#
#     graph = go.Scatter(
#         x=x,
#         y=y,
#         name='Manipulate Graph'
#         )
#     layout = go.Layout(
#         paper_bgcolor='#27293d',
#         plot_bgcolor='rgba(0,0,0,0)',
#         xaxis=dict(range=[min(x), max(x)]),
#         yaxis=dict(range=[min(y), max(y)]),
#         font=dict(color='white'),
#
#         )
#     return {'data': [graph], 'layout': layout}
