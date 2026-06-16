import logo from './logo.svg';
import './App.css';

function App() {
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
