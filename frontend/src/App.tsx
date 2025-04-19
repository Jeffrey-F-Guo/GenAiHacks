import { useState } from 'react'
import './App.css'
import MapComponent from './components/GoogleMap'

function App() {
  return (
    <div className="app-container">
      <h1 className="app-title">Venture Map</h1>
      <p className="app-subtitle">Discover new places and activities near you</p>
      
      {/* Map */}
      <MapComponent />
      
    </div>
  )
}

export default App