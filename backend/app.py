from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os #gets the API key instead of having it hardcoded
import json
import requests  # NEW: For making HTTP requests to Spotify API

app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# Spotify credentials from environment variables
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# NEW: Function to get Spotify access token
def get_spotify_token():
    """Get Spotify access token"""
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')

    # NEW: Function to search for a song on Spotify
def search_spotify_track(song_title, artist_name):
    """Search for a track on Spotify and return preview URL"""
    token = get_spotify_token()
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": f"track:{song_title} artist:{artist_name}",
        "type": "track",
        "limit": 1
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if data['tracks']['items']:
        track = data['tracks']['items'][0]
        return {
            "preview_url": track.get('preview_url'),  # 30-second preview
            "spotify_url": track['external_urls']['spotify']
        }
    return None

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    mood = data.get('mood')
    activity = data.get('activity')

    prompt = f"""
    Recommend 5 afrobeats songs for someone who is feeling {mood} while {activity}.
    Return ONLY valid JSON in this format:
    {{"songs":[
    {{"title": "Song name", "artist": "Artist name"}}
    ]}}
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        text = response.choices[0].message.content
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        recommendations = json.loads(text)
        
        # NEW: Loop through each song and add Spotify preview URL
        for song in recommendations['songs']:
            spotify_data = search_spotify_track(song['title'], song['artist'])
            if spotify_data:
                song['preview_url'] = spotify_data['preview_url']  # NEW: 30-second audio preview
                song['spotify_url'] = spotify_data['spotify_url']  # NEW: Link to full song
        
        return jsonify(recommendations)
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)