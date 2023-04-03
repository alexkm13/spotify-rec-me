import os
from flask import Flask, request, redirect, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import rec
from json import jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)

sp_oauth = SpotifyOAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="your_redirect_uri",
    scope="user-library-read"
)

@app.route("/")

def index():
    token_info = session.get("token_info", None)
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    else:
        sp = spotipy.Spotify(auth=token_info["access_token"])
        results = sp.current_user_saved_tracks()
        return str(results)
@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/")


def recommend():
    user_tracks = request.json['tracks']
    tracks = rec.get_saved_tracks()
    df = rec.create_dataframe(tracks)
    knn = rec.train_knn(df)
    
    # Get recommendations for the user's tracks
    recommendations = []
    for track in user_tracks:
        distances, indices = knn.kneighbors([track])
        recommendations.extend(indices[0])
    recommended_tracks = df.iloc[recommendations].to_dict(orient='records')
    return jsonify(recommended_tracks)

if __name__ == '__main__':
    app.run(debug=True)