import React from 'react';
import { categories } from '../constants';

interface ResultsSectionProps {
  showResults: boolean;
  resultsRef: React.RefObject<HTMLDivElement>;
  isMobile: boolean;
  selectedCategories: string[];
  radiusInMiles: number;
}

const ResultsSection: React.FC<ResultsSectionProps> = ({
  showResults,
  resultsRef,
  isMobile,
  selectedCategories,
  radiusInMiles,
}) => {
  if (!showResults) return null;

  return (
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
  );
};

export default ResultsSection; 