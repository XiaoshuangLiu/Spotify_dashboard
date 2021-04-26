import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import plotly.express as px
import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
import dash_table

df1 = pd.read_csv('data/cleaned_artists.csv')
df2 = pd.read_csv('data/cleaned_tracks.csv')

genre_list = df1.new_genre.unique()
artist_list = df1.name.unique()
year_list = df2.sort_values('year', ascending=False).year.unique()

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Top 50 Artists and Their Top Tracks"),
            html.H3("Welcome to the Music Analytics Dashboard"),
            html.Div(
                id="intro",
                children="The dashboard summarizes the information of Spotify's top 50 most streamed artists of 2020 globally and their top tracks. By selecting the music genre you like, you can find the most popular artists in that genre and the top 10 popular track list. You can customize the list by adding or removing artists and selecting different music release years.",
            ),
        ],
    )

fig  = px.bar(df1[df1.new_genre == genre_list[0]][['name','followers','popularity']].drop_duplicates().sort_values('followers', ascending=False), x = 'name', y = 'followers', color = 'popularity' )
fig.update_layout(
    xaxis_title="Artist",
    yaxis_title="Artist Follower",
    font=dict(size=12),
    xaxis_tickangle=-45
)
fig.show()

def generate_barplot(df1):  
    fig  = px.bar(df1[['name','followers','popularity']].drop_duplicates().sort_values('followers', ascending=False), x = 'name', y = 'followers', color = 'popularity', title="Artist Followers & Popularity", 
                  labels={'artist_follower':'Artist Follower', 'name': 'Artist'})
    fig.update_layout(
        xaxis_title="Artist",
        yaxis_title="Artist Follower",
        font=dict(size=12)
    )
    fig.show()
    return fig

tb = df2.loc[df2.artists_name.isin(df1[df1.new_genre == df1.new_genre[0]].name)].sort_values('popularity', ascending = False)[['name', 'artists_name','external_urls','popularity','album_name','year']].drop_duplicates(subset=['name']).head(20)

data_columns = ['Track Name', 'Artist', 'URL', 'Popularity', 'Album', 'Year']
df_columns = ['name', 'artists_name', 'external_urls', 'popularity', 'album_name', 'year']

app = dash.Dash(__name__)


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("Spotify_Logo_CMYK_Green.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="three columns",
            children=[description_card(), 
                                 
                      html.P("Select Music Genre", style={'textAlign': 'left','font-weight': 'bold'}),
                        dcc.Dropdown(
                            id="genre-select",
                            options=[{"label": i, "value": i} for i in genre_list],
                            value=genre_list[0],
                                 style={'width': '100%'}
                        ),
                        html.Br(),
                        html.Br(),
                        html.P("Select Artists", style={'textAlign': 'left','font-weight': 'bold'}),
                        dcc.Dropdown(
                            id="artist-select",
                            options=[{"label": i, "value": i} for i in artist_list],
                            value=artist_list[:],
                            multi=True,
                        ),
                        html.Br(),
                        html.Br(),
                        html.P("Music Release Year", style={'textAlign': 'left','font-weight': 'bold'}),
                        dcc.Checklist(
                            id="year-picker-select",
                            options=[{"label": i, "value": i} for i in year_list],
                            value=year_list[:],
                            style={"display":"inline-flex", "flex-wrap":"wrap", "line-height":"28px"},
                        ), 
                     ],),
         html.Br(),
        # Right column
        html.Div(
            id="right-column",
            className="nine columns",
            children=[
                # popularity barplot
                html.Div(
                    id="barplot_section",
                    children=[
                        html.B("Most Followed Artists"),
                        html.Hr(),
                        dcc.Graph(id="popularity_barplot", figure = fig),
                    ],
                ),
                 html.Br(),
                # top 10 track table
                html.Div(
                    id="table_section",
                    children=[
                        html.B("Top 20 Popular Tracks"),
                        html.Hr(),
                        dash_table.DataTable(
                            id='table',
                             columns=[{
                              'name': col, 
                              'id': df_columns[idx]
                            } for (idx, col) in enumerate(data_columns)],
                            data=tb.to_dict('records'),
                            style_cell=dict(textAlign='left'),
                            style_header=dict(backgroundColor="lightgrey", fontWeight='bold'),
                            style_data=dict(backgroundColor="white")
                        )
                    ],
                ),
            ],
        ),
    ]
        )

@app.callback(
    Output(component_id = 'artist-select', component_property = 'value'),
    [Input(component_id = 'genre-select', component_property = 'value')]
)
def update_artist(options_chosen):
    artist_list = df1[df1.new_genre == options_chosen].name.unique()
    return artist_list


@app.callback(
    Output(component_id = 'year-picker-select', component_property = 'value'),
    [Input(component_id = 'artist-select', component_property = 'value')]
)
def update_year(options_chosen):
    year_list = df2[df2.artists_name.isin(options_chosen)].sort_values('year', ascending = False).year.unique()
    return year_list

@app.callback(
    Output(component_id = 'popularity_barplot', component_property = 'figure'),
    [Input(component_id = 'artist-select', component_property = 'value')]
)
def update_barplot(options_chosen):
    dfs = df1[df1.name.isin(options_chosen)]
    df_all = dfs[['name','followers','popularity']].drop_duplicates().sort_values('followers', ascending= False)
    fig  = px.bar(df_all, x = 'name', y = 'followers', color = 'popularity')
    fig.update_layout(
        xaxis_title="Artist",
        yaxis_title="Artist Follower",
        font=dict(size=12),
        xaxis_tickangle=-45
    )
    return fig


@app.callback(
    Output(component_id = 'table', component_property = 'data'),
    [Input(component_id = 'artist-select', component_property = 'value'),
    Input(component_id = 'year-picker-select', component_property = 'value')],
)
def update_table(name,year):
    tb = df2.loc[(df2.artists_name.isin(name)) &(df2.year.isin(year))].sort_values('popularity', ascending = False)[['name', 'artists_name','external_urls','popularity','album_name','year']].drop_duplicates(subset=['name']).head(20)
    tb = tb.to_dict('records')
    return tb

server = app.server

# Run the server
if __name__ == "__main__":
    app.run_server(debug=False)