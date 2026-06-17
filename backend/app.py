from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import os #gets the API key instead of having it hardcoded
import json

app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))



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
        return jsonify(recommendations)
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)