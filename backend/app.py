from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai   #for the google gemini
import os #gets the API key instead of having it hardcoded
import json

app = Flask(__name__)
CORS(app)
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')


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
        response = model.generate_content(prompt)
        text = response.text
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        recommendations = json.loads(text)  # converts strings to python dictionary
        return jsonify(recommendations)  # converts python dictionary to JSON string
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500







if __name__ == '__main__':
    app.run(debug=True, port=5000)