import React, { useState, useEffect, useRef, useCallback } from 'react';
import { GoogleMap, LoadScript, Marker, Autocomplete } from '@react-google-maps/api';

// Fixed height for the map container
const mapContainerStyle = {
  width: '100%',
  height: '405px', // Fixed height to match options section
  borderRadius: '12px',
};

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

interface ChatMessage {
  sender: 'user' | 'agent';
  text: string;
  timestamp: Date;
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
  const [notesValue, setNotesValue] = useState<string>('');
  const [radiusInMiles, setRadiusInMiles] = useState<number>(5);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['entertainment']);
  const [isMobile, setIsMobile] = useState<boolean>(window.innerWidth < 1024);
  const [showResults, setShowResults] = useState<boolean>(false);
  
  // Chat state
  const [showChat, setShowChat] = useState<boolean>(false);
  const [minimizeChat, setMinimizeChat] = useState<boolean>(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      sender: 'agent',
      text: 'Hi there! I\'m Venture, your personal guide. Need help exploring the places I found for you?',
      timestamp: new Date()
    }
  ]);
  const [chatInput, setChatInput] = useState<string>('');
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  // References
  const mapRef = useRef<google.maps.Map | null>(null);
  const circleRef = useRef<google.maps.Circle | null>(null);
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);
  const resultsRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll chat to bottom when new messages arrive
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages]);

  // Load API key
  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string;
    setApiKey(key || '');
    if (!key) {
      setError('API key not found. Check your .env file.');
    }

    const handleResize = () => {
      setIsMobile(window.innerWidth < 1024);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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

      // Calculate and set appropriate zoom level
      const bounds = new google.maps.LatLngBounds();
      const center = new google.maps.LatLng(markerPosition.lat, markerPosition.lng);
      const north = google.maps.geometry.spherical.computeOffset(center, radiusInMeters, 0);
      const south = google.maps.geometry.spherical.computeOffset(center, radiusInMeters, 180);
      const east = google.maps.geometry.spherical.computeOffset(center, radiusInMeters, 90);
      const west = google.maps.geometry.spherical.computeOffset(center, radiusInMeters, 270);
      
      bounds.extend(north);
      bounds.extend(south);
      bounds.extend(east);
      bounds.extend(west);
      
      // Use proper padding type for fitBounds
      const padding: google.maps.Padding = {
        top: 50,
        right: 50,
        bottom: 50,
        left: 50
      };
      
      mapRef.current.fitBounds(bounds, { padding });
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
    setInputValue(place.formatted_address || '');
    updateMapPosition(place.geometry.location);
  };

  const handleEnterKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (window.google && window.google.maps && inputValue.trim()) {
        const geocoder = new window.google.maps.Geocoder();
        geocoder.geocode({ address: inputValue }, (results, status) => {
          if (status === 'OK' && results && results[0]) {
            updateMapPosition(results[0].geometry.location);
          } else {
            setError('Location not found. Try a different address.');
          }
        });
      }
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

  // Handle search button click
  const handleSearch = () => {
    if (inputValue.trim() && window.google && window.google.maps) {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: inputValue }, (results, status) => {
        if (status === 'OK' && results && results[0]) {
          updateMapPosition(results[0].geometry.location);
          setShowResults(true);
          // Show chat when search is successful
          setShowChat(true);
          // Scroll to results after a short delay to ensure DOM is updated
          setTimeout(() => {
            resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
          }, 100);
        } else {
          setError('Location not found. Try a different address.');
        }
      });
    } else if (!inputValue.trim()) {
      setError('Please enter a location to search.');
    } else {
      setShowResults(true);
      // Show chat when search is successful
      setShowChat(true);
      // Scroll to results after a short delay to ensure DOM is updated
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  };

  // Handle sending a chat message
  const handleSendMessage = () => {
    if (chatInput.trim()) {
      // Add user message
      const userMessage: ChatMessage = {
        sender: 'user',
        text: chatInput,
        timestamp: new Date()
      };
      
      setChatMessages(prev => [...prev, userMessage]);
      setChatInput(''); // Clear input
      
      // Simulate agent response after a short delay
      setTimeout(() => {
        const responseText = generateAgentResponse(chatInput);
        
        const agentMessage: ChatMessage = {
          sender: 'agent',
          text: responseText,
          timestamp: new Date()
        };
        
        setChatMessages(prev => [...prev, agentMessage]);
      }, 1000);
    }
  };

  // Handle chat input keypress (for Enter key)
  const handleChatKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Simple response generator based on user input
  const generateAgentResponse = (input: string): string => {
    const lowerInput = input.toLowerCase();
    
    if (lowerInput.includes('restaurant') || lowerInput.includes('food') || lowerInput.includes('eat')) {
      return `Based on your preferences, I'd recommend trying Place 1 or Place 3 for food. Place 1 is closer to your current location and has great reviews!`;
    } else if (lowerInput.includes('activity') || lowerInput.includes('things to do') || lowerInput.includes('entertainment')) {
      return `There are several entertainment options nearby! Place 2 has amazing activities, and it's within your selected radius. Would you like more specific details?`;
    } else if (lowerInput.includes('directions') || lowerInput.includes('how to get') || lowerInput.includes('navigate')) {
      return `I can help with directions! From your current location, the fastest route to Place 1 is via Main Street. It should take about 10 minutes by car or 25 minutes by public transport.`;
    } else if (lowerInput.includes('review') || lowerInput.includes('rating')) {
      return `Place 1 has 4.5 stars based on 240 reviews. Place 2 has 4.2 stars from 185 reviews. Place 3 has 4.7 stars but only 95 reviews. Place 4 has 4.0 stars from 310 reviews.`;
    } else if (lowerInput.includes('hours') || lowerInput.includes('open') || lowerInput.includes('close')) {
      return `Most places in this area are open from 10am to 9pm. Place 2 stays open late until 11pm on Friday and Saturday. Place 4 opens early at 8am.`;
    } else if (lowerInput.includes('thank')) {
      return `You're welcome! Happy to help. Let me know if you need anything else for your adventure!`;
    } else if (lowerInput.includes('hello') || lowerInput.includes('hi ')) {
      return `Hello there! How can I help with your search results? I can tell you more about any of these places or suggest which ones might suit your preferences best.`;
    } else {
      return `That's a great question about the area! Based on your search, I'd recommend checking out Place 2 first as it best matches your interests. Can I help you with anything specific about these locations?`;
    }
  };

  return apiKey ? (
    <LoadScript googleMapsApiKey={apiKey} libraries={['places']}>
      <div className="map-container" style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        gap: '4px',
        marginBottom: '60px',
        position: 'relative'
      }}>
        {/* Main Map Explorer Container */}
        <div
          className="map-explorer"
          style={{
            backgroundColor: '#fff',
            borderRadius: '24px',
            padding: '32px',
            width: '100%',
            maxWidth: '1200px',
            margin: '0 auto',
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
              >
                {/* Search bar */}
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
                    mapContainerStyle={mapContainerStyle}
                    center={center}
                    zoom={11}
                    onLoad={onMapLoad}
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
              </div>

              {/* Right side - Options */}
              <div 
                style={{ 
                  flex: isMobile ? 'auto' : 1, 
                  width: '100%',
                  height: isMobile ? 'auto' : '400px', // Match height with map
                }}
              >
                {/* Options Section */}
                <div 
                  className="options-section"
                  style={{
                    backgroundColor: '#f0f7ff',
                    padding: '24px',
                    borderRadius: '16px',
                    border: '1px solid #d1e4ff',
                    minWidth: isMobile ? 'auto' : '250px',
                    boxSizing: 'border-box',
                    width: '100%',
                    height: isMobile ? 'auto' : '475px', // Medium height
                    display: 'flex',
                    flexDirection: 'column',
                  }}
                >
                  <h2 style={{ 
                    fontSize: '22px', 
                    marginTop: 0, 
                    marginBottom: '20px',
                    color: '#1e40af',
                    fontWeight: 600,
                    textAlign: 'center'
                  }}>
                    Options
                  </h2>
                  
                  <div style={{ 
                    display: 'flex', 
                    flexDirection: 'column', 
                    gap: '16px',
                    flex: 1 // Fill available space
                  }}>
                    {/* Radius Slider */}
                    <div style={{ padding: '0 10px' }}>
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
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
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
                        gap: '10px',
                        flex: 1,
                        marginBottom: '10px'
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
              </div>
            </div>

            {/* Notes section and Search button */}
            <div style={{ 
              display: 'flex', 
              flexDirection: isMobile ? 'column' : 'row',
              gap: '16px',
              alignItems: isMobile ? 'stretch' : 'flex-end',
              justifyContent: 'space-between',
              marginTop: '0px' // Removed margin completely
            }}>
              <div style={{ flex: '1' }}>
                <div style={{
                  backgroundColor: '#f0f7ff',
                  padding: '24px',
                  borderRadius: '16px',
                  border: '1px solid #d1e4ff',
                }}>
                  <h2 style={{ 
                    fontSize: '22px', 
                    marginTop: 0, 
                    marginBottom: '20px',
                    color: '#1e40af',
                    fontWeight: 600,
                    textAlign: 'left'
                  }}>
                    Additional Information
                  </h2>
                  <textarea
                    placeholder="Add any additional notes or preferences..."
                    value={notesValue}
                    onChange={(e) => setNotesValue(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '16px',
                      borderRadius: '12px',
                      border: '1px solid #d1d5db',
                      minHeight: '80px',
                      fontSize: '16px',
                      resize: 'vertical',
                      backgroundColor: '#f9fafb',
                      color: '#111',
                      boxSizing: 'border-box',
                    }}
                  />
                </div>
              </div>
              <button
                onClick={handleSearch}
                style={{
                  backgroundColor: '#2563eb',
                  color: 'white',
                  border: 'none',
                  borderRadius: '12px',
                  padding: '16px 32px',
                  fontSize: '16px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  height: 'fit-content',
                  boxShadow: '0 4px 6px rgba(37, 99, 235, 0.1)',
                  whiteSpace: 'nowrap',
                }}
              >
                Search
              </button>
            </div>

            {error && <div style={{ color: 'red', marginTop: '8px' }}>{error}</div>}
          </div>
        </div>

        {/* Results section - Separate container and only shown after search */}
        {showResults && (
          <div
            ref={resultsRef}
            style={{
              backgroundColor: '#fff',
              borderRadius: '24px',
              padding: '32px',
              width: '100%',
              maxWidth: '1200px',
              margin: '32px auto 0',
              boxShadow: '0 12px 28px rgba(0,0,0,0.08)',
            }}
          >
            <div
              style={{
                backgroundColor: '#f0f7ff',
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
                      {/* Show categories in each place card */}
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
          </div>
        )}
        
        {/* Chat Widget */}
        {showChat && (
          <div
            style={{
              position: 'fixed',
              bottom: '20px',
              right: '20px',
              width: minimizeChat ? '60px' : '350px',
              height: minimizeChat ? '60px' : '400px',
              backgroundColor: '#fff',
              borderRadius: '16px',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
              overflow: 'hidden',
              zIndex: 1000,
              display: 'flex',
              flexDirection: 'column',
              transition: 'all 0.3s ease',
              border: '1px solid #d1e4ff',
            }}
          >
            {/* Chat Header */}
            <div
              style={{
                backgroundColor: '#2563eb',
                padding: minimizeChat ? '10px' : '16px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                color: 'white',
                cursor: 'pointer',
              }}
              onClick={() => setMinimizeChat(!minimizeChat)}
            >
              <div style={{ display: 'flex', alignItems: 'center' }}>
                {!minimizeChat && (
                  <span style={{ 
                    backgroundColor: '#1d4ed8', 
                    borderRadius: '50%', 
                    width: '32px', 
                    height: '32px', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    marginRight: '12px',
                  }}>
                    🧭
                  </span>
                )}
                <span style={{ 
                  fontWeight: 600, 
                  fontSize: minimizeChat ? '0' : '16px', 
                  transition: 'font-size 0.3s ease',
                  whiteSpace: 'nowrap'
                }}>
                  Venture Assistant
                </span>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'white',
                    cursor: 'pointer',
                    padding: '4px',
                    fontSize: '18px',
                    fontWeight: 'bold',
                    lineHeight: 1,
                  }}
                  onClick={(e) => {
                    e.stopPropagation();
                    setMinimizeChat(!minimizeChat);
                  }}
                >
                  {minimizeChat ? '↗' : '↘'}
                </button>
                <button
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'white',
                    cursor: 'pointer',
                    padding: '4px',
                    fontSize: '18px',
                    fontWeight: 'bold',
                    lineHeight: 1,
                  }}
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowChat(false);
                  }}
                >
                  ×
                </button>
              </div>
            </div>

                          {/* Chat Messages */}
            {!minimizeChat && (
              <div
                style={{
                  flex: 1,
                  overflowY: 'auto',
                  padding: '16px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px',
                  backgroundColor: '#f8fafc',
                }}
              >
                {chatMessages.map((message, index) => (
                  <div
                    key={index}
                    style={{
                      alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
                      maxWidth: '80%',
                      backgroundColor: message.sender === 'user' ? '#2563eb' : 'white',
                      color: message.sender === 'user' ? 'white' : '#374151',
                      padding: '12px 16px',
                      borderRadius: message.sender === 'user' 
                        ? '16px 16px 4px 16px' 
                        : '16px 16px 16px 4px',
                      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                      border: message.sender === 'user' 
                        ? 'none' 
                        : '1px solid #e2e8f0',
                      fontSize: '14px',
                      lineHeight: 1.5,
                    }}
                  >
                    {message.text}
                  </div>
                ))}
                <div ref={chatEndRef} />
              </div>
            )}

            {/* Chat Input */}
            {!minimizeChat && (
              <div
                style={{
                  padding: '12px 16px',
                  borderTop: '1px solid #e2e8f0',
                  display: 'flex',
                  gap: '8px',
                  backgroundColor: 'white',
                }}
              >
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={handleChatKeyPress}
                  placeholder="Ask about the places..."
                  style={{
                    flex: 1,
                    padding: '10px 14px',
                    borderRadius: '20px',
                    border: '1px solid #d1d5db',
                    fontSize: '14px',
                    outline: 'none',
                    backgroundColor: '#f9fafb',
                  }}
                />
                <button
                  onClick={handleSendMessage}
                  style={{
                    backgroundColor: '#2563eb',
                    color: 'white',
                    border: 'none',
                    borderRadius: '50%',
                    width: '36px',
                    height: '36px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer',
                    flexShrink: 0,
                  }}
                >
                  →
                </button>
              </div>
            )}
          </div>
        )}
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