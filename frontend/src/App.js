import logo from './logo.svg';
import './App.css';
import {useState, useEffect} from 'react';

function App() {
  const[mood, setMood] = useState(null)
  const[activity, setActivity] = useState(null)
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchRecommendations = async() => {
    if(!activity.trim()){
      setError("Please tell me what you are doing");
      return;ss
    }
    setLoading(true);
    setError('');
    
  }
  return (
    <div>
      <div className='row'>
      <label className = "mood" htmlFor = "mood">Mood:</label>
      <select id="mood" name="mood">
      <option value = "happy">Happy</option>
      <option value = "sad">Sad</option>
      <option value = "energetic"> Energetic</option>
      <option value = "chill">Chill</option>
      <option value = "party">Party</option>
      </select>
    </div>
    
    <div className='row'>
      <label className='activity' htmlFor='activity'>What are you doing?</label>
      <input type = "text" id="activity" placeholder='e.g., working, driving' />
    </div>
    
    <div>
      <button className='search-btn'>Search Recommendations</button>
    </div>

    </div>
  )
   
}

export default App;
