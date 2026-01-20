from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# API Access Functions

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


token = get_token()

# Search Functions

def search_for_artist(artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print("No artist found")
        return None
    
    return json_result[0]

def search_for_song(song_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    if (artist_name is None):
        query = f"?q={song_name}&type=track&limit=1"
    else:
        query = f"?q={song_name}%20{artist_name}&type=track&limit=1"
    
    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["tracks"]["items"]

    if len(json_result) == 0:
        print("No song found")
        return None

    return json_result[0]

# Get Functions

def get_songs_by_artist(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_song_features(song_id):
    url = f"https://api.spotify.com/v1/audio-features/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)
    return json_result

# Testing

result = search_for_artist("BIBI")
artist_id = result["id"]
songs = get_songs_by_artist(artist_id)

song_result = search_for_song("Rise & Fall", "JUNNY")
song_id = song_result["id"]
song_features = get_song_features(song_id)
print(song_features)
print(song_id)