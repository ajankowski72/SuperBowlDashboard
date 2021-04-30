"""
Dashboard created in lecture Week 11
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def generate_tablee(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)
superbowl = pd.read_csv("teams.csv", index_col=0)
pie = pd.read_csv("finalsuperbowl.csv", index_col=0)
titles = ['Super Bowl Locations by State', 'Super Bowl Locations by City', 'Super Bowls by Winning Score', 'Super Bowls by Losing Score', 'Super Bowls by Margin of Victory', "Super Bowl MVP's by Player", "Super Bowl MVP's by Position"]

fig = px.bar(superbowl, x = 'Team', y = 'Super Bowl Wins', color = 'Team', title='Super Bowl Wins By NFL Team')
fig2 = px.pie(pie, names = 'State', values = 'State', color='State')

checklist_labels = [{'label' : team, 'value' : team} for team in superbowl.Team]

app.layout = html.Div([
    html.H1('Super Bowl History Dashboard',
            style={'textAlign' : 'center'}),
    html.A("Click here to view the NFL's website",
           href='http://www.nfl.com',
           target='_blank'),
    dcc.Graph(figure=fig, id='sb_plot'),
    html.Div([html.H4('Teams to Display:'),
    dcc.Checklist(options=checklist_labels,
                  value=['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Colts', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Los Angeles Chargers', 'Los Angeles Raiders', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets', 'Oakland Raiders', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'St. Louis Rams', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Redskins' ],
                  id = 'team_checklist')],
             style={'width':'49%', 'float' : 'left'}),
    html.Div(id='table_div'),
    html.Label(['Super Bowl Demographics']),
    dcc.Dropdown(
            options=[
            {'label': 'Super Bowls by State', 'value': 'State'},
            {'label': 'Super Bowls by City', 'value': 'City'},
            {'label': "Super Bowls by Winning Team's Points", 'value': "Winning Team's Points"},
            {'label': "Super Bowls by Losing Team's Points", 'value': "Losing Team's Points"},
            {'label': 'Super Bowls by Margin of Victory', 'value': 'Margin of Victory'},
            {'label': "Super Bowls by MVP", 'value': 'MVP'},
            {'label': "Super Bowls by MVP's Position", 'value': "MVP's Position"}
        ],
        value='State',
        id = 'my_dropdown',
        multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    dcc.Graph(figure=fig2, id='pie_plot'),
    html.Div(id='master_div',
        style={'width':'49%', 'float' : 'left'})
        ])

@app.callback(
    Output(component_id="table_div", component_property="children"),
    [Input(component_id="team_checklist", component_property="value")]
)
def update_table(teams):
    x = superbowl[superbowl.Team.isin(teams)].sort_values('Team')
    return generate_table(x)

@app.callback(
    Output(component_id="sb_plot", component_property="figure"),
    [Input(component_id="team_checklist", component_property="value")]
)
def update_plot(teams):
    df2 = superbowl[superbowl.Team.isin(teams)].sort_values('Team', ascending=True)
    fig = px.bar(df2, x="Team", y="Super Bowl Wins", color="Team", title='Super Bowl Wins By NFL Team')
    return fig

@app.callback(
    Output(component_id="master_div", component_property="children"),
    [Input(component_id="my_dropdown", component_property="value")]
)
def update_tablee(master):
    y = pie
    return generate_tablee(y)

@app.callback(
    Output(component_id='pie_plot', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def update_graph(my_dropdown):
    
    piechart=px.pie(
            data_frame=pie,
            names=my_dropdown,
            title = 'Super Bowls by ' + my_dropdown
            )

    return (piechart)



server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=3005)
    





