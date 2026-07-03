from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import json
import re
import random

app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# Map artists to their real songs
ARTIST_SONGS = {
    "wizkid": ["Essence", "Ojuelegba", "Joro", "Come Closer", "Soco"],
    "burna boy": ["Last Last", "Ye", "On The Low", "Anybody"],
    "rema": ["Calm Down", "Dumebi", "Soundgasm"],
    "davido": ["Fall", "If", "Assurance", "Fia"],
    "ayra starr": ["Rush", "Bloody Samaritan"],
    "ckay": ["Love Nwantiti", "Emiliana"],
    "fireboy dml": ["Peru", "Scatter", "Bandana"],
    "olamide": ["Dangote", "Wo", "Caro"],
    "kizz daniel": ["Buga", "Fever", "Lie"],
    "joeboy": ["Baby", "Alcohol", "Sip"],
    "tems": ["Free Mind", "Damages", "Try Me"],
    "mavins": ["Overdue", "Rosemary", "Closer"],
}

def extract_json(text):
    """Extract JSON from Groq response"""
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if json_match:
        text = json_match.group(1)
    
    json_match = re.search(r'(\{[\s\S]*\})', text)
    if json_match:
        text = json_match.group(1)
    
    return text

def get_song_for_artist(artist_name):
    """Get a random real song for an artist"""
    artist_lower = artist_name.lower().strip()
    
    # Try to match artist to our list
    for known_artist, songs in ARTIST_SONGS.items():
        if known_artist in artist_lower or artist_lower in known_artist:
            return random.choice(songs)
    
    # If artist not found, return a random song from any artist
    all_songs = []
    for songs in ARTIST_SONGS.values():
        all_songs.extend(songs)
    return random.choice(all_songs)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    mood = data.get('mood')
    activity = data.get('activity')

    prompt = f"""
    Recommend exactly 5 REAL afrobeats ARTISTS for someone who is feeling {mood} while {activity}.

    CRITICAL RULES:
    1. ONLY recommend REAL artists who actually exist
    2. Choose from well-known, popular Afrobeats artists
    3. Mix up the artists (don't repeat)

    Examples of REAL artists: Wizkid, Burna Boy, Rema, Davido, Ayra Starr, CKay, Fireboy DML, Olamide, Kizz Daniel

    Return ONLY valid JSON in this format:
    {{"artists": ["Artist 1", "Artist 2", "Artist 3", "Artist 4", "Artist 5"]}}
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        
        text = response.choices[0].message.content
        print("Raw Groq response:", text)
        
        cleaned_text = extract_json(text)
        print("Cleaned JSON:", cleaned_text)
        
        data = json.loads(cleaned_text)
        
        artists = data.get('artists', [])
        print(f"Artists received: {artists}")
        
        # Map each artist to a real song
        songs = []
        used_artists = set()
        
        for artist in artists[:5]:
            # Clean artist name
            clean_artist = artist.strip()
            # Get a song for this artist
            song_title = get_song_for_artist(clean_artist)
            songs.append({
                "title": song_title,
                "artist": clean_artist
            })
            used_artists.add(clean_artist.lower())
        
        # If we have less than 5, fill with fallback artists
        fallback_artists = ["Wizkid", "Burna Boy", "Davido", "Rema", "Ayra Starr", "CKay", "Fireboy DML", "Olamide", "Kizz Daniel"]
        
        while len(songs) < 5:
            for artist in fallback_artists:
                if len(songs) >= 5:
                    break
                if artist.lower() not in used_artists:
                    song_title = get_song_for_artist(artist)
                    songs.append({
                        "title": song_title,
                        "artist": artist
                    })
                    used_artists.add(artist.lower())
        
        # Shuffle the songs for variety
        random.shuffle(songs)
        
        final_songs = songs[:5]
        print(f"Returning {len(final_songs)} songs")
        
        return jsonify({"songs": final_songs})
    
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        print(f"Raw text that failed: {text}")
        return jsonify({"error": "Failed to parse JSON from LLM"}), 500
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)