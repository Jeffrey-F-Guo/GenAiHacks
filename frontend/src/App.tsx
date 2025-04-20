import { useState } from 'react'
import './App.css'
import MapComponent from './components/GoogleMap'

function App() {
  const [savedNote, setSavedNote] = useState<string>('');

  const handleNoteSave = (note: string) => {
    setSavedNote(note);
    // You can use the saved note elsewhere in your application if needed
    console.log('Note saved:', note);
  };

  return (
    <div className="app-container">
      <div className="title-section">
        <h1 className="app-title">Venture Map</h1>
        <div className="title-underline"></div>
        <p className="app-subtitle">A smart web app that finds the top 4 places based on a selected area, radius, and selected activity categories</p>
      </div>
      
      {/* Map */}
      <MapComponent />
      
    </div>
  )
}

export default App