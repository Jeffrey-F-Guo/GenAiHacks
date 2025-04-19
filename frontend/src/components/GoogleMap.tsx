import React, { useState, useEffect, useRef, useCallback } from 'react';
import { GoogleMap, LoadScript, Marker, Autocomplete } from '@react-google-maps/api';

// Dynamic container style
const getContainerStyle = (optionsHeight: number) => ({
  width: '100%',
  height: '500px',
  borderRadius: '12px',
});

const initialCenter = {
  lat: 37.7749,
  lng: -122.4194,
};

// Interface definitions
interface CategoryType {
  id: string;
  label: string;
  icon: string;
}

const categories: CategoryType[] = [
  { id: 'entertainment', label: 'Entertainment', icon: '🎭' },
  { id: 'food', label: 'Food', icon: '🍽️' },
  { id: 'shopping', label: 'Shopping', icon: '🛍️' },
  { id: 'explore', label: 'Explore', icon: '🧭' },
  { id: 'wellness', label: 'Wellness', icon: '💆' },
];

function MapComponent() {
  const [center, setCenter] = useState(initialCenter);
  const [markerPosition, setMarkerPosition] = useState(initialCenter);
  const [apiKey, setApiKey] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [inputValue, setInputValue] = useState<string>('');
  const [radiusInMiles, setRadiusInMiles] = useState<number>(5);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['entertainment']);
  const [isMobile, setIsMobile] = useState<boolean>(window.innerWidth < 1024);
  const [optionsHeight, setOptionsHeight] = useState<number>(0);
  const [showResults, setShowResults] = useState<boolean>(false);

  // We'll only use the map reference directly
  const mapRef = useRef<google.maps.Map | null>(null);
  const circleRef = useRef<google.maps.Circle | null>(null);
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);
  const optionsSectionRef = useRef<HTMLDivElement | null>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const searchButtonRef = useRef<HTMLButtonElement | null>(null);

  // Load API key
  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string;
    setApiKey(key || '');
    if (!key) {
      setError('API key not found. Check your .env file.');
    }

    const handleResize = () => {
      setIsMobile(window.innerWidth < 1024);
      updateOptionsHeight();
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Update options height
  useEffect(() => {
    updateOptionsHeight();
    const timer = setTimeout(updateOptionsHeight, 100);
    return () => clearTimeout(timer);
  }, [selectedCategories, isMobile]);

  const updateOptionsHeight = () => {
    if (optionsSectionRef.current && searchButtonRef.current && !isMobile) {
      const optionsHeight = optionsSectionRef.current.offsetHeight;
      const buttonHeight = searchButtonRef.current.offsetHeight;
      const totalHeight = optionsHeight + buttonHeight + 16; // 16px for gap
      setOptionsHeight(totalHeight);
    } else {
      setOptionsHeight(400); // Default height for mobile
    }
  };

  // Function to handle map load
  const onMapLoad = useCallback((map: google.maps.Map) => {
    mapRef.current = map;
    
    // Create the initial circle
    updateCircle(radiusInMiles);
  }, [radiusInMiles]);

  // Function to update or create the circle
  const updateCircle = useCallback((radius: number) => {
    const radiusInMeters = radius * 1609.34;
    
    // If a circle already exists, remove it
    if (circleRef.current) {
      circleRef.current.setMap(null);
      circleRef.current = null;
    }
    
    // Only create a new circle if radius is greater than 0 and map exists
    if (radius > 0 && mapRef.current) {
      // Circle options
      const circleOptions: google.maps.CircleOptions = {
        strokeColor: '#4285F4',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: 'rgba(66, 133, 244, 0.15)',
        fillOpacity: 0.35,
        map: mapRef.current,
        center: markerPosition,
        radius: radiusInMeters
      };
      
      // Create a new circle
      circleRef.current = new google.maps.Circle(circleOptions);
    }
  }, [markerPosition]);

  // Update circle when radius changes
  useEffect(() => {
    updateCircle(radiusInMiles);
  }, [radiusInMiles, updateCircle]);

  // Update circle when position changes
  useEffect(() => {
    if (circleRef.current) {
      circleRef.current.setCenter(markerPosition);
    }
  }, [markerPosition]);

  // Clean up circle on unmount
  useEffect(() => {
    return () => {
      if (circleRef.current) {
        circleRef.current.setMap(null);
        circleRef.current = null;
      }
    };
  }, []);

  const updateMapPosition = (location: google.maps.LatLng) => {
    const newPos = {
      lat: location.lat(),
      lng: location.lng(),
    };
    
    setCenter(newPos);
    setMarkerPosition(newPos);
    
    // Update circle position
    if (circleRef.current) {
      circleRef.current.setCenter(newPos);
    }
    
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

    if (window.google && window.google.maps) {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: inputValue }, (results, status) => {
        if (status === 'OK' && results && results[0]) {
          updateMapPosition(results[0].geometry.location);
          // Show results after search
          setShowResults(true);
        } else {
          setError('Location not found. Try a different address.');
        }
      });
    }
  };

  const handleEnterKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleManualSearch();
    }
  };

  // Multi-select category toggle
  const handleCategoryToggle = (categoryId: string) => {
    setSelectedCategories(prev => {
      if (prev.includes(categoryId)) {
        return prev.filter(id => id !== categoryId);
      } else {
        return [...prev, categoryId];
      }
    });
  };

  // Handle radius slider change
  const handleRadiusChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newRadius = Number(e.target.value);
    setRadiusInMiles(newRadius);
  };

  return apiKey ? (
    <LoadScript googleMapsApiKey={apiKey} libraries={['places']}>
      <div
        className="map-explorer"
        style={{
          backgroundColor: '#fff',
          borderRadius: '24px',
          padding: '32px',
          width: '100%',
          maxWidth: '1200px',
          margin: '0 auto 60px auto',
          boxShadow: '0 12px 28px rgba(0,0,0,0.08)',
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Map and Options in a flex container */}
          <div
            style={{
              display: 'flex',
              flexDirection: isMobile ? 'column' : 'row',
              gap: '24px',
              alignItems: 'flex-start',
            }}
          >
            {/* Left side - Map and Search */}
            <div 
              style={{ 
                flex: isMobile ? 'auto' : 3, 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '16px',
                width: '100%'
              }}
              ref={mapContainerRef}
            >
              {/* Search bar - now exactly as wide as the map */}
              <Autocomplete
                onLoad={(ref) => (autocompleteRef.current = ref)}
                onPlaceChanged={handlePlaceChanged}
                options={{ types: ['geocode', 'establishment'] }}
              >
                <input
                  type="text"
                  placeholder="Select a location"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleEnterKey}
                  style={{
                    width: '100%',
                    padding: '16px 20px',
                    borderRadius: '12px',
                    border: '1px solid #ccc',
                    fontSize: '16px',
                    backgroundColor: '#f3f4f6',
                    color: '#111',
                    boxSizing: 'border-box',
                  }}
                />
              </Autocomplete>

              {/* Map */}
              <div style={{ width: '100%' }}>
                <GoogleMap
                  mapContainerStyle={getContainerStyle(optionsHeight)}
                  center={center}
                  zoom={14}
                  onLoad={onMapLoad}
                  options={{
                    zoomControl: true,
                    streetViewControl: false,
                    mapTypeControl: true,
                    fullscreenControl: true,
                  }}
                >
                  <Marker position={markerPosition} />
                  {/* No Circle component here - we manage it directly */}
                </GoogleMap>
              </div>
            </div>

            {/* Right side - Options on top with Search Button below */}
            <div style={{ flex: isMobile ? 'auto' : 1, display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {/* Options Section now on top */}
              <div 
                ref={optionsSectionRef}
                className="options-section"
                style={{
                  backgroundColor: '#f0f7ff',
                  padding: '24px',
                  borderRadius: '16px',
                  border: '1px solid #d1e4ff',
                  minWidth: isMobile ? 'auto' : '250px',
                  boxSizing: 'border-box',
                  width: '100%',
                }}
              >
                <h2 style={{ 
                  fontSize: '22px', 
                  marginTop: 0, 
                  marginBottom: '20px',
                  color: '#1e40af',
                  fontWeight: 600
                }}>
                  Options
                </h2>
                
                <div style={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  gap: '24px'
                }}>
                  {/* Radius Slider */}
                  <div style={{ marginTop: '20px', padding: '0 10px' }}>
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center',
                      marginBottom: '8px'
                    }}>
                      <label style={{ 
                        fontWeight: 500,
                        color: '#374151',
                        fontSize: '14px'
                      }}>
                        Search Radius
                      </label>
                      <div style={{
                        fontSize: '14px',
                        fontWeight: 600,
                        color: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        padding: '4px 8px',
                        borderRadius: '6px'
                      }}>
                        {radiusInMiles} {radiusInMiles === 1 ? 'mile' : 'miles'}
                      </div>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="50"
                      value={radiusInMiles}
                      onChange={handleRadiusChange}
                      style={{
                        width: '100%',
                        height: '6px',
                        borderRadius: '3px',
                        background: '#e5e7eb',
                        outline: 'none',
                        transition: 'all 0.3s ease',
                        WebkitAppearance: 'none',
                        cursor: 'pointer'
                      }}
                    />
                  </div>
                  
                  {/* Categories - with multi-select */}
                  <div>
                    <p style={{ 
                      marginBottom: '10px',
                      fontWeight: 500,
                      color: '#4b5563'
                    }}>
                      Categories: <span style={{ fontSize: '13px', color: '#6b7280' }}>(select all that apply)</span>
                    </p>
                    <div style={{ 
                      display: 'flex', 
                      flexDirection: 'column', 
                      gap: '10px'
                    }}>
                      {categories.map(category => (
                        <button
                          key={category.id}
                          onClick={() => handleCategoryToggle(category.id)}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            padding: '10px 16px',
                            borderRadius: '8px',
                            border: '1px solid #d1d5db',
                            backgroundColor: selectedCategories.includes(category.id) 
                              ? '#2563eb' 
                              : 'white',
                            color: selectedCategories.includes(category.id)
                              ? 'white'
                              : '#4b5563',
                            cursor: 'pointer',
                            fontSize: '15px',
                            fontWeight: 500,
                            transition: 'all 0.2s ease',
                            textAlign: 'left'
                          }}
                        >
                          <span>{category.icon}</span>
                          <span>{category.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Search button now below options */}
              <button
                ref={searchButtonRef}
                onClick={() => {
                  handleManualSearch();
                  setShowResults(true);
                }}
                style={{
                  backgroundColor: '#2563eb',
                  color: 'white',
                  border: 'none',
                  borderRadius: '12px',
                  padding: '16px 24px',
                  fontSize: '16px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  width: '100%',
                }}
              >
                Search
              </button>

              {error && <div style={{ color: 'red', marginTop: '8px' }}>{error}</div>}
            </div>
          </div>

          {/* Results section - only shown after search */}
          {showResults && (
            <div
              style={{
                backgroundColor: '#f0f7ff', // Light blue background
                borderRadius: '16px',
                padding: '24px',
                border: '1px solid #d1e4ff',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '16px'
                }}
              >
                <h2
                  style={{
                    margin: 0,
                    fontSize: '24px',
                    fontWeight: 700,
                    color: '#1e40af',
                  }}
                >
                  Top Places to Explore
                </h2>
                <div
                  style={{
                    display: 'flex',
                    gap: '12px'
                  }}
                >
                  <span
                    style={{
                      fontSize: '13px',
                      padding: '6px 12px',
                      backgroundColor: '#dbeafe',
                      borderRadius: '20px',
                      color: '#1e40af',
                      fontWeight: 500,
                    }}
                  >
                    {selectedCategories.length} {selectedCategories.length === 1 ? 'category' : 'categories'}
                  </span>
                  <span
                    style={{
                      fontSize: '13px',
                      padding: '6px 12px',
                      backgroundColor: '#dbeafe',
                      borderRadius: '20px',
                      color: '#1e40af',
                      fontWeight: 500,
                    }}
                  >
                    {radiusInMiles} {radiusInMiles === 1 ? 'mile' : 'miles'} radius
                  </span>
                </div>
              </div>
              <div 
                style={{ 
                  display: 'grid',
                  gridTemplateColumns: isMobile 
                    ? '1fr' 
                    : 'repeat(auto-fill, minmax(250px, 1fr))',
                  gap: '20px' 
                }}
              >
                {[1, 2, 3, 4].map((num) => (
                  <div
                    key={num}
                    style={{
                      backgroundColor: 'white',
                      borderRadius: '14px',
                      padding: '20px',
                      fontSize: '16px',
                      fontWeight: 500,
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
                      border: '1px solid #e5e7eb',
                      color: '#374151',
                    }}
                  >
                    <div style={{ 
                      display: 'flex', 
                      flexDirection: 'column',
                      gap: '8px',
                      alignItems: 'flex-start',
                      textAlign: 'left'
                    }}>
                      <h3 style={{ margin: 0, fontSize: '18px' }}>
                        Place {num}
                      </h3>
                      <p style={{ margin: 0, color: '#6b7280', fontSize: '14px' }}>123 Example Street</p>
                      <div style={{ 
                        display: 'flex', 
                        gap: '6px',
                        flexWrap: 'wrap',
                        marginTop: '4px'
                      }}>
                        {selectedCategories.map(catId => (
                          <span 
                            key={catId}
                            style={{
                              fontSize: '13px',
                              padding: '4px 8px',
                              backgroundColor: '#f3f4f6',
                              borderRadius: '6px',
                              color: '#4b5563'
                            }}
                          >
                            {categories.find(c => c.id === catId)?.icon} {categories.find(c => c.id === catId)?.label}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
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
