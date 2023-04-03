import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Replace these with your own client ID and secret
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

# Step 1: Get access token
auth_url = 'https://accounts.spotify.com/api/token'
auth_data = {'grant_type': 'client_credentials'}
auth_response = requests.post(auth_url, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), data=auth_data)
access_token = auth_response.json()['access_token']

# Step 2: Get user's saved songs
def get_saved_songs(access_token, user_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    saved_songs_url = f'https://api.spotify.com/v1/users/{user_id}/tracks'
    response = requests.get(saved_songs_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error fetching saved songs: {response.status_code} {response.text}')

# Replace this with the user's Spotify ID
user_id = 'user_spotify_id'
saved_songs = get_saved_songs(access_token, user_id)

# create a dataframe for the tracks
def create_dataframe(tracks):
    track_data = []
    for track_obj in tracks:
        track = track_obj['track']
        track_data.append([track['id'], track['name'], track['artists'][0]['name']])
    df = pd.DataFrame(track_data, columns=['id', 'name', 'artist'])
    return df

d = create_dataframe(saved_songs)

# train k-nn to output the best recommendations
def train_knn(df):
    # You'll need to extract features from the tracks and add them to the DataFrame.
    knn = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
    knn.fit(df)
    return knn

train_knn(d)
