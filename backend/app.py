from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import json
import random

app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# The list of real songs
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
    "tiwa savage": ["Somebody's Son", "Koroba", "49-99", "All Over"],
    "mr eazi": ["Leg Over", "Pour Me Water", "Skin Tight"],
    "tekno": ["Pana", "Duro", "Skeletun"],
    "yemi alade": ["Johnny", "Oh My Gosh", "Tumbum"],
    "flavour": ["Bia", "Nwa Baby", "Baby Na Yoka"],
    "omah lay": ["Godly", "Bad Influence", "Understand"],
    "ruger": ["Bounce", "Dior", "Girlfriend"]
}

# The backend will ONLY accept activities containing these words
VALID_ACTIVITIES = [
    "work", "working", "study", "studying", "drive", "driving", "gym", 
    "working out", "run", "running", "cook", "cooking", "clean", "cleaning",
    "relax", "relaxing", "chill", "chilling", "sleep", "sleeping", "party",
    "partying", "dance", "dancing", "commute", "commuting", "travel", 
    "traveling", "read", "reading", "write", "writing", "code", "coding", 
    "game", "gaming", "play", "playing", "exercise", "exercising"
]

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    mood = data.get('mood')
    activity = data.get('activity').lower().strip()

    # BACKEND GATEKEEPER: Check if the activity is valid
    is_valid = any(word in activity for word in VALID_ACTIVITIES)
    
    if not is_valid:
        print(f"Rejected activity: {activity}")
        return jsonify({"songs": []})

    prompt = f"""
    You are an expert Afrobeats DJ. 
    The user is feeling {mood} and is currently doing this activity: {activity}.

    Think carefully about the vibe of this specific activity:
    - If they are studying/working, choose chill, focus-friendly artists (e.g., Tems, Fireboy DML, Omah Lay).
    - If they are driving/partying, choose high-energy, fast-tempo artists (e.g., Rema, Burna Boy, Ruger).
    - If they are sad, choose emotional, deep artists (e.g., Joeboy, Omah Lay).

    Recommend exactly 5 REAL afrobeats ARTISTS that perfectly match this specific vibe.
    """
    
    try:
        # USING JSON SCHEMA MODE
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b", 
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "artist_recommendations",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "artists": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "A list of exactly 5 Afrobeats artist names."
                            }
                        },
                        "required": ["artists"]
                    }
                }
            }
        )
        
        # Because we used JSON Schema, the response is GUARANTEED to be clean JSON.
        # We don't even need regex to extract it anymore!
        result = json.loads(response.choices[0].message.content)
        artists = result.get('artists', [])
        print("Artists returned by AI:", artists)
        
        songs = []
        
        # Pair the artist and song together
        for artist in artists[:5]:
            clean_artist = artist.strip().lower()
            
            # Check if we have this artist in our list
            for known_artist, known_songs in ARTIST_SONGS.items():
                if known_artist in clean_artist or clean_artist in known_artist:
                    # Pick ONE song for this specific artist
                    random_song = random.choice(known_songs)
                    songs.append({
                        "title": random_song, 
                        "artist": artist.strip()
                    })
                    break
        
        return jsonify({"songs": songs})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)