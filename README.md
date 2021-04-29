# MA705 Final Project: Spotify_dashboard

This repository contains files used in the MA705 dashboard project. 
The final dashboard is deployed on Heroku [here](https://xiaoshuang.herokuapp.com/).

## Dashboard Description

The dashboard summarizes the information of Spotify's top 50 most streamed artists of 2020 globally and their top tracks. By selecting the music genre you like, you can find the most popular artists in that genre and the top 10 popular track list. You can customize the list by adding or removing artists and music release years.

## Data Sources

The Top 50 artist list is from [CHART DATA](https://chartdata.org/2020/12/02/spotifys-top-50-artists-of-2020/).
The data is collected from the [Spotify API](https://developer.spotify.com/documentation/web-api/reference/#category-artists) according to the top 50 artists list. You can find the data scraping code on data scraping and cleaning.py file. The file will generate two raw csv file: raw_artists.csv and raw_tracks.csv. After data cleaning, two cleaned csv file were exported. The variables in each dataframe are listed below.


### cleaned_artists.csv

- id
- name
- followers
- popularity
- new_genre

### cleaned_tracks.csv

- album_name	
- album_release_date
- artists_name
- artists_id
- duration_ms
- explicit	
- name
- popularity
- external_urls
- year
