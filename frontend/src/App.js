import './App.css';
import { useState } from 'react';

function App() {
  const [mood, setMood] = useState('happy');
  const [activity, setActivity] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    if (!activity.trim()) {
      setError("Please tell me what you are doing");
      return;
    }
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:5000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood, activity })
      });
      if (!response.ok) {
        throw new Error("failed to get recommendations");
      }

      const data = await response.json();
      setRecommendations(data.songs || []);
    } catch (err) {
      setError("Error recommending");
      console.log("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className='row'>
        <label className="mood" htmlFor="mood">Mood:</label>
        <select id="mood" name="mood" value={mood} onChange={(e) => setMood(e.target.value)}>
          <option value="happy">Happy</option>
          <option value="sad">Sad</option>
          <option value="energetic">Energetic</option>
          <option value="chill">Chill</option>
          <option value="party">Party</option>
        </select>
      </div>

      <div className='row'>
        <label className='activity' htmlFor='activity'>What are you doing?</label>
        <input type="text" id="activity" placeholder='e.g., working, driving' value={activity} onChange={(e) => setActivity(e.target.value)} />
      </div>

      <div>
        <button className='search-btn' onClick={fetchRecommendations} disabled={loading}>
          {loading ? "Searching ..." : "Search recommendations"}
        </button>
      </div>

      {error && <div className='error'>{error}</div>}

      {recommendations.length > 0 && (
        <div className="results">
          <h3>🎵 Recommendations</h3>
          {recommendations.map((song, index) => (
            <div key={index} className="song-card">
              <div className="song-info">
                <span className="song-number">{index + 1}.</span>
                <span className="song-title">{song.title}</span>
                <span className="song-artist">by {song.artist}</span>
              </div>
              <a 
                href={`https://www.youtube.com/results?search_query=${encodeURIComponent(song.title + ' ' + song.artist)}`}
                target="_blank" 
                rel="noopener noreferrer"
                className="youtube-link"
              >
                ▶️ Listen on YouTube
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;