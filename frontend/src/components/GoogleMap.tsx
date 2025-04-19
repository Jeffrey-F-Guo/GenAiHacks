import React, { useState, useEffect, useRef } from 'react';
import { GoogleMap, LoadScript, Marker, Autocomplete } from '@react-google-maps/api';

const containerStyle = {
  width: '500px',
  height: '500px',
  borderRadius: '12px',
};

const initialCenter = {
  lat: 37.7749,
  lng: -122.4194,
};

declare global {
  interface Window {
    google: any;
  }
}

function MapComponent() {
  const [center, setCenter] = useState(initialCenter);
  const [markerPosition, setMarkerPosition] = useState(initialCenter);
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [inputValue, setInputValue] = useState('');

  const autocompleteRef = useRef<any>(null);

  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
    setApiKey(key || '');
    if (!key) {
      setError('API key not found. Check your .env file.');
    }
  }, []);

  const updateMapPosition = (location: google.maps.LatLng) => {
    const newPos = {
      lat: location.lat(),
      lng: location.lng(),
    };
    setCenter(newPos);
    setMarkerPosition(newPos);
    setError('');
  };

  const handlePlaceChanged = () => {
    const place = autocompleteRef.current?.getPlace();
    if (!place || !place.geometry) {
      setError('Place not found.');
      return;
    }
    updateMapPosition(place.geometry.location);
  };

  const handleManualSearch = () => {
    if (!inputValue.trim()) return;

    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ address: inputValue }, (results: any, status: any) => {
      if (status === 'OK' && results[0]) {
        updateMapPosition(results[0].geometry.location);
      } else {
        setError('Location not found. Try a different address.');
      }
    });
  };

  const handleEnterKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleManualSearch();
    }
  };

  return apiKey ? (
    <LoadScript googleMapsApiKey={apiKey} libraries={['places']}>
      <div
        className="map-explorer"
        style={{
          backgroundColor: '#fff',
          borderRadius: '24px',
          padding: '48px',
          maxWidth: '100%',
          margin: '60px auto',
          boxShadow: '0 12px 28px rgba(0,0,0,0.08)',
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '36px' }}>
          {/* Search bar */}
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            <Autocomplete
              onLoad={(ref) => (autocompleteRef.current = ref)}
              onPlaceChanged={handlePlaceChanged}
            >
              <input
                type="text"
                placeholder="Select a location"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleEnterKey}
                style={{
                  flex: 1,
                  minWidth: '400px',
                  padding: '20px 24px',
                  borderRadius: '12px',
                  border: '1px solid #ccc',
                  fontSize: '18px',
                  backgroundColor: '#f3f4f6',
                  color: '#111',
                }}
              />
            </Autocomplete>
            <button
              onClick={handleManualSearch}
              style={{
                backgroundColor: '#2563eb',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                padding: '20px 36px',
                fontSize: '18px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Search
            </button>
          </div>

          {error && <div style={{ color: 'red' }}>{error}</div>}

          {/* Map and Places */}
          <div
            style={{
              display: 'flex',
              flexDirection: window.innerWidth < 768 ? 'column' : 'row',
              gap: '48px',
            }}
          >
            {/* Map section */}
            <div style={{ flex: 3 }}>
              <GoogleMap
                mapContainerStyle={containerStyle}
                center={center}
                zoom={14}
                options={{
                  zoomControl: true,
                  streetViewControl: false,
                  mapTypeControl: true,
                  fullscreenControl: true,
                }}
              >
                <Marker position={markerPosition} />
              </GoogleMap>
            </div>

            {/* Right-side Places */}
            <div style={{ flex: 2 }}>
              <h2
                style={{
                  marginTop: 0,
                  marginBottom: '24px',
                  fontSize: '28px',
                  fontWeight: 700,
                  color: '#111827',
                }}
              >
                Top Places to Explore
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {[1, 2, 3, 4].map((num) => (
                  <div
                    key={num}
                    style={{
                      backgroundColor: 'white',
                      borderRadius: '14px',
                      padding: '20px 24px',
                      fontSize: '18px',
                      fontWeight: 500,
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
                      border: '1px solid #e5e7eb',
                      color: '#374151',
                      textAlign: 'center',
                    }}
                  >
                    Address {num}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </LoadScript>
  ) : (
    <div
      style={{
        height: '500px',
        backgroundColor: '#e5e7eb',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: '12px',
      }}
    >
      Loading map...
    </div>
  );
}

export default MapComponent;
