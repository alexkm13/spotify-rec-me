import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import pull_id

# authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               client_secret="YOUR_CLIENT_SECRET",
                                               redirect_uri="YOUR_REDIRECT_URI",
                                               scope="user-library-read"))
# get user's saved tracks
results = sp.current_user_saved_tracks()
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# create dataframe of track features
track_features = []
for track in tracks:
    features = sp.audio_features(track['track']['id'])[0]
    features['id'] = track['track']['id']
    features['name'] = track['track']['name']
    features['artist'] = track['track']['artists'][0]['name']
    track_features.append(features)
df = pd.DataFrame(track_features)
df = df.dropna()

# fit Nearest Neighbors model
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(df.drop(['id', 'name', 'artist'], axis=1))

# get recommendations for a song
def get_recommendations(song):
    song_id = pull_id.get_id(song) 
    song_features = sp.audio_features(song_id)[0]
    return nn.kneighbors([song_features])[1][0]


#  print(f"{i}. {df.iloc[recommendations[i]][['name', 'artist']].values[0]}")