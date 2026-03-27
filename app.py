# Import packages
from turtle import title

from dash import Dash, State, dcc, Input, Output
import dash_bootstrap_components as dbc

# Initialise the App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Create app components
markdown = dcc.Markdown(id='our-markdown', children='Text', style={'fontSize': 24})
selector = dcc.RadioItems(id='our-colorselector',
                            options=[
                                {'label': 'Red', 'value': 'red'},
                                {'label': 'Green', 'value': 'green'},
                                {'label': 'Blue', 'value': 'blue'}
                            ], value='red')

# App Layout
app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col([markdown], width=8)]),
        dbc.Row(
            [
                dbc.Col([selector], width=9),
            ]
        ),
    ]
)

# Callbacks
@app.callback(
    Output(component_id='our-markdown', component_property='style'),
    Input(component_id='our-colorselector', component_property='value'),
    State(component_id='our-markdown', component_property='style')
)
def update_markdown(value_selector, current_style):
    style = current_style.copy()
    style['color'] = value_selector
    return style

# Run the App
if __name__ == '__main__':
    app.run(debug=False)
