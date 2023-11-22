from dash import Dash, dcc, html, Input, Output
from plots import *
from pre_process import *

# for test in computer do not have connection to the data add test=True in create_df parameters
df = create_df()
fig = combine_all_daily_plots(df)
fig.update_layout(autosize=False, height=1080, width=1920)

app = Dash(__name__)
server=app.server

app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig),
    dcc.Clipboard(target_id="structure"),
    html.Pre(
        id='structure',
        style={
            'overflowY': 'auto',
            'height': '100vw',
            'width': '100hw'
        }
    ),
])
