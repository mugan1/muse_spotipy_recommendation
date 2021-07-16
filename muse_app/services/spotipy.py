import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from muse_app.utils.song_cluster import get_pipeline

cid = 'a5df1b77b9674396a7e07dcad3ae1544'
secret = '47d0b180565643b6bb9e83a507f489c2'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artists(name) :
   search = sp.search(name, limit=5, type='artist')
   get_artist_info = []
   for i in range(0, search['artists']['limit']) :
      get_artist_info.append([search['artists']['items'][i]['name'], search['artists']['items'][i]['genres'], search['artists']['items'][i]['popularity']])
      
   return get_artist_info

def get_tracks(name) :
   search = sp.search(name, limit=50, type='track')
   get_track_info = []
   for i in range(0, search['tracks']['limit']) :
      get_track_info.append([search['tracks']['items'][i]['name'], search['tracks']['items'][i]['artists'][0]['name'], search['tracks']['items'][i]['album']['release_date']])

   return get_track_info

def get_artist_track(name) :
    search =sp.search(name, limit=1, type='artist')
    result = sp.search(q= 'artist: {}'.format(name), limit=50)
    get_track_info = []
    for i in range(0, result['tracks']['limit']) :
        get_track_info.append([result['tracks']['items'][i]['name'], result['tracks']['items'][i]['artists'][0]['name'], result['tracks']['items'][i]['album']['release_date']])
    return get_track_info

# recommend system

def find_song(name, year):
    song_data = dict()
    results = sp.search(q= 'track: {} year: {}'.format(name,year), limit=1)
    if results['tracks']['items'] == []:
        return None

    results = results['tracks']['items'][0]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)

def get_song_data(song, spotify_data):
    
    try:
        song_data = spotify_data[(spotify_data['name'] == song['name']) 
                                & (spotify_data['year'] == song['year'])].iloc[0]
        return song_data
    
    except IndexError:
        return find_song(song['name'], song['year'])
        
number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

def get_mean_vector(song_list, spotify_data):
    
    song_vectors = []
    
    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)  
    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)


def flatten_dict_list(dict_list):
    
    flattened_dict = dict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

def recommend_songs( song_list, spotify_data, n_songs=100):

    metadata_cols = ['name', 'year', 'artists']
    song_dict = flatten_dict_list(song_list)
    song_center = get_mean_vector(song_list, spotify_data)
    scaler = get_pipeline().steps[0][1]
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data)
    index = list(np.argsort(distances)[:, :n_songs][0])
    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]

    return rec_songs[metadata_cols].to_dict(orient='records')

def find_feature(name, year):
    song_data = dict()
    results = sp.search(q= 'track: {} year: {}'.format(name,year), limit=1)
    if results['tracks']['items'] == []:
        return None

    results = results['tracks']['items'][0]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]
    for key in ['id','mode', 'analysis_url', 'duration_ms', 'time_signature','track_href','type','uri', 'key', 'tempo'] :
      audio_features.pop(key)
    for key, value in audio_features.items():
        song_data[key] = value
    return pd.DataFrame(song_data, index=[0])

def feature_dict(list):
    for l in list :
        song_data = find_feature(l.track, l.released)
        features = pd.DataFrame()
        features = features.append(song_data)
    features_mean = dict(features.mean())

    return features_mean

