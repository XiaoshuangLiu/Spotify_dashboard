import requests
import pandas as pd
import numpy as np
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

access_token = 'BQAhG-KB_TU5tZWRo6p5JDQr6a0udHfgxsaMbQ1y_4lc17ctwqy8OlI5eRPhoR_ynbomfTnF-u9oEcE-G5NjLEWa8hB92EvXD2uoiZQ9WdAkyKaXGfOQMF_Y8-gSvTfPyP8ADZQNWy5JWN7ycS0fPiNDRkc34gk'

Artist_IDs = ['4q3ewBCX7sLwd24euuV69X', '3TVXtAsR1Inumwj472S9r4', '1vyhD5VmyZ7KMfW5gqLgo5','4MCBfE4596Uoi2O4DtmEMz', '1Xyo4u8uXC1ZmMpatF05PJ',
'3Nrfpe0tUJi4K4DXYWgMUX','6qqNVTkY8uBg9cP3Jd7DAH','06HL4z0CvFAxyc27GXpf02','246dkjvS1zLTtiykXe5h60','0Y5tJX1MQlPlqiwlOH1tJY',
'66CXWjxzNUsdJxJ2JdwvnR','1uNFoZAHBGtllmzznpCI3s','7dGJo4pcD2V6oG8kP0tJRR','2R21vXR83lH98kGeO99Y66','6M2wZ9GZgrQXHCFfjv46we',
'1i8SpTcr7yvPOmcqrbnVXY','6eUKZXaKkcviH0Ku9w2n3V','15UsOTVnJzReFVN1VCnxy4','6LuN9FCkKOj5PcnpouEgny','4VMYDCV2IEDYJArk749S6m',
'4SsVbpTthjScTS7U2hmr1X','0eDvMgVFoNV3TpwtrVCoTj','4r63FhuTkUYltbVAg5TQnk','6KImCVD70vtIoJWnq6nGn3','4O15NlyKLIASxsJ0PrXPfz',
'26VFTg2z8YR0cCuwLzESi2','1HY2Jd0NmPuamShAr6KMms','7iK8PXO48WeuP03g8YR51W','1mcTU81TzQhprhouKaTkpq','757aE44tKEUQEqRuT6GnEB',
'5K4W6rqBFWDnAN6FQUkS6x','1r4hJ1h58CWwUQe3MxPuau','04gDigrS5kc9YWfZHwBETP','1dfeR4HaWDbWqFHLkxsg1d','0hCNtLu0JehylgoiP8L4Gh',
'4AK6F7OLvEQ5QYCBNiQWHq','1RyvyyTE3xzB2ZywiAwp0i','329e4yvIujISKGKz1BZZbO','53XhwfbYqKCa1cC15pYq2q','64KEffDW9EtZ1y2vBYgq8T',
'7n2wHs1TKAczGzO7Dd2rGr','5pKCCKE2ajJHZ9KAiaK11H','3WrFJ7ztbogyGnTHbHJFl2','4gzpq5DPGxSnKTe4SA8HAU','2wY79sveU1sp5g7SokKOiI',
'4GNC7GD6oZMSxPGyXy4MNB','4nDoRrQiYLoBzwC5BhVJzF','0C8ZW7ezQVs4URX5aX7Kqx', '5cj0lLjcoR7YOSnhnX0Po5','23fqKkggKUBHNkbKtXEls4']


df1 = pd.DataFrame()
for ID in Artist_IDs:
    url = f'https://api.spotify.com/v1/artists/{ID}'
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    req = requests.get(url, headers=headers)
    data = req.json()
    
    lines = []
    for genre in data['genres']:
        line = {'id': data['id'], 
                'name': data['name'],
                'genre': genre,
                'followers': data['followers']['total'], 
                'popularity': data['popularity'] }
        lines.append(line)
    df1 = df1.append(lines, ignore_index=True)

df1.to_csv('data/raw_artists.csv', index = False)

df2 = pd.DataFrame()
for ID in Artist_IDs:
    url = f'https://api.spotify.com/v1/artists/{ID}/top-tracks?market=US'
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    req = requests.get(url, headers=headers)
    data = req.json()

    lines = []
    for track in data['tracks']:
        for artist in track['artists']:
            line = {'album_name': track['album']['name'], 
                    'album_release_date': track['album']['release_date'],
                    'artists_name': artist['name'], 
                    'artists_id': artist['id'] }
            for k in ['duration_ms', 'explicit', 'name', 'popularity']:
                line[k] = track[k]
            line['external_urls'] = track['external_urls']['spotify']
            lines.append(line)
    df2 = df2.append(lines, ignore_index=True)

df2.to_csv('data/raw_tracks.csv', index = False)


# clean artist data

df1 = pd.read_csv('data/raw_artists.csv')

df1['new_genre'] = np.where(df1.genre.str.contains('hip hop|r&b|urban contemporary'), 'Hiphop', '')
df1['new_genre'] = np.where(df1.genre.str.contains('pop|british invasion|merseybeat|boy band|talent show|beatlesque'),  'Pop', df1['new_genre'] )
df1['new_genre'] = np.where(df1.genre.str.contains('rock|permanent wave'),'Rock', df1['new_genre'] )
df1['new_genre'] = np.where(df1.genre.str.contains('latin|latino|reggaeton|tropical'), 'Latino', df1['new_genre'] )
df1['new_genre'] = np.where(df1.genre.str.contains('rap'), 'Rap', df1['new_genre'] )
df1['new_genre'] = np.where(df1.genre.str.contains('drill|trap'), 'Trap', df1['new_genre'] )
df1['new_genre'] = np.where(df1.genre.str.contains('house|edm|brostep'), 'House', df1['new_genre'])

df1

df1 = df1[['id','name'	,'followers','popularity','new_genre']].drop_duplicates()
df1

df1.to_csv('data/cleaned_artists.csv', index=False)


# clean track data
df2 = pd.read_csv('data/raw_tracks.csv')
df2
artist_list = df1.name.unique()
artist_list
df2.artists_name.nunique()
df2 = df2[df2['test'] == 'yes']
df2
df2['year'] = df2['album_release_date'].str.split('-').str[0]
df2.to_csv('data/cleaned_tracks.csv', index=False)

genres = " ".join(str(genre) for genre in df1.new_genre)
genres

wordcloud = WordCloud(width=800, height=400,max_words=30, background_color="white").generate(genres)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
#plt.savefig('/content/drive/MyDrive/Colab Notebooks/plot/Wordcloud.png', dpi=128)
plt.show()