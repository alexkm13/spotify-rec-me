import re

def get_id(song):
    spotify_link = song
    song_id = re.findall(r"track/(\w+)", spotify_link)[0]
    return song_id