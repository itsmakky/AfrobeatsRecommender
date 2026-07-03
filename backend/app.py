from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import json
import re
import random
from database import get_song_for_artist  # ← CHANGED: Import from database

app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def extract_json(text):
    """Extract JSON from Groq response"""
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if json_match:
        text = json_match.group(1)
    
    json_match = re.search(r'(\{[\s\S]*\})', text)
    if json_match:
        text = json_match.group(1)
    
    return text

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
    4. Return EXACTLY 5 artists

    Examples of REAL artists: Wizkid, Burna Boy, Rema, Davido, Ayra Starr, CKay, Fireboy DML, Olamide, Kizz Daniel, Joeboy, Tems

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
        
        # Map each artist to a real song from MongoDB
        songs = []
        used_artists = set()
        
        for artist in artists[:5]:
            clean_artist = artist.strip()
            song_title = get_song_for_artist(clean_artist)  # ← CHANGED: Uses MongoDB
            print(f"Artist: {clean_artist} → Song: {song_title}")
            songs.append({
                "title": song_title,
                "artist": clean_artist
            })
            used_artists.add(clean_artist.lower())
        
        # Fallback if less than 5 songs
        fallback_artists = ["Wizkid", "Burna Boy", "Davido", "Rema", "Ayra Starr", "CKay", "Fireboy DML", "Olamide", "Kizz Daniel", "Joeboy", "Tems"]
        
        if len(songs) < 5:
            print(f"Only {len(songs)} artists from LLM. Filling with fallback...")
            for artist in fallback_artists:
                if len(songs) >= 5:
                    break
                if artist.lower() not in used_artists:
                    song_title = get_song_for_artist(artist)  # ← CHANGED: Uses MongoDB
                    songs.append({
                        "title": song_title,
                        "artist": artist
                    })
                    used_artists.add(artist.lower())
                    print(f"Fallback: {artist} → Song: {song_title}")
        
        random.shuffle(songs)
        final_songs = songs[:5]
        print(f"Returning {len(final_songs)} songs")
        
        return jsonify({"songs": final_songs})
    
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        return jsonify({"error": "Failed to parse JSON from LLM"}), 500
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)