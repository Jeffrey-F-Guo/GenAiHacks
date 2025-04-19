import React from 'react';
import { GoogleMap, LoadScript } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '400px'
};

// Set this to your desired location coordinates
const center = {
  lat: 37.7749,
  lng: -122.4194
};

function MapComponent() {
  // Access the Maps API key from environment variables
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
  
  return (
    <div>
      <h2>My Google Map</h2>
      <LoadScript googleMapsApiKey={apiKey}>
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={center}
          zoom={10}
        >
          {/* You can add markers, polygons, etc. here */}
        </GoogleMap>
      </LoadScript>
    </div>
  );
}

export default MapComponent;