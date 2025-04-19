import React, { useState, useEffect } from 'react';

interface NoteComponentProps {
  onNoteSave?: (note: string) => void;
}

function NoteComponent({ onNoteSave }: NoteComponentProps) {
  const [note, setNote] = useState<string>('');
  const [savedNote, setSavedNote] = useState<string>('');
  const [showSaved, setShowSaved] = useState<boolean>(false);

  // Load saved note from localStorage on component mount
  useEffect(() => {
    const savedNoteFromStorage = localStorage.getItem('venture-map-note');
    if (savedNoteFromStorage) {
      setSavedNote(savedNoteFromStorage);
      setShowSaved(true);
    }
  }, []);

  const handleNoteChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setNote(e.target.value);
  };

  const handleSaveNote = () => {
    if (note.trim()) {
      // Save to state
      setSavedNote(note);
      setShowSaved(true);
      
      // Save to localStorage
      localStorage.setItem('venture-map-note', note);
      
      // Call the callback if provided
      if (onNoteSave) {
        onNoteSave(note);
      }
      
      // Clear the input
      setNote('');
    }
  };

  const handleClearNote = () => {
    setSavedNote('');
    setShowSaved(false);
    localStorage.removeItem('venture-map-note');
  };

  return (
    <div
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
      <h2 style={{ 
        fontSize: '24px', 
        marginTop: 0, 
        marginBottom: '20px',
        color: '#1e40af',
        fontWeight: 600,
        textAlign: 'left'
      }}>
        Trip Informaiton
      </h2>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <textarea
          placeholder="Add notes about your trip or places you want to visit..."
          value={note}
          onChange={handleNoteChange}
          style={{
            width: '100%',
            height: '120px',
            padding: '16px 20px',
            borderRadius: '12px',
            border: '1px solid #ccc',
            fontSize: '16px',
            backgroundColor: '#f3f4f6',
            color: '#111',
            boxSizing: 'border-box',
            fontFamily: 'inherit',
            resize: 'vertical',
          }}
        />
        
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button
            onClick={handleSaveNote}
            style={{
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              padding: '12px 20px',
              fontSize: '16px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Save Note
          </button>
        </div>
        
        {showSaved && savedNote && (
          <div 
            style={{
              marginTop: '16px',
              backgroundColor: '#f0f7ff',
              padding: '20px',
              borderRadius: '12px',
              border: '1px solid #d1e4ff',
            }}
          >
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'flex-start',
              marginBottom: '8px'
            }}>
              <h3 style={{ 
                margin: 0, 
                fontSize: '18px', 
                color: '#1e40af',
                fontWeight: 600,
                textAlign: 'left'
              }}>
                Saved Information
              </h3>
              <button
                onClick={handleClearNote}
                style={{
                  backgroundColor: 'transparent',
                  color: '#6b7280',
                  border: 'none',
                  padding: '4px 8px',
                  fontSize: '14px',
                  cursor: 'pointer',
                }}
              >
                Clear
              </button>
            </div>
            <p style={{ 
              whiteSpace: 'pre-wrap',
              textAlign: 'left',
              margin: 0,
              color: '#374151',
            }}>
              {savedNote}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default NoteComponent;