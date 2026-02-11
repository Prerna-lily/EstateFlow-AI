import React from 'react';
import { Star, Phone, MapPin, Home, TrendingUp, Trash2 } from 'lucide-react';
import { propertyService } from '../services/api';

const PropertyList = ({ properties, loading, onUpdate }) => {
  const handleToggleFavorite = async (id) => {
    try {
      await propertyService.toggleFavorite(id);
      onUpdate();
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this property?')) {
      try {
        await propertyService.deleteProperty(id);
        onUpdate();
      } catch (error) {
        console.error('Error deleting property:', error);
      }
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading properties...</p>
      </div>
    );
  }

  if (properties.length === 0) {
    return (
      <div className="empty-state">
        <Home size={48} />
        <h3>No Properties Found</h3>
        <p>Try adjusting your filters or add a new property</p>
      </div>
    );
  }

  return (
    <div className="property-list">
      <div className="list-header">
        <h2>Properties ({properties.length})</h2>
      </div>

      <div className="property-grid">
        {properties.map((property) => (
          <PropertyCard
            key={property.id}
            property={property}
            onToggleFavorite={handleToggleFavorite}
            onDelete={handleDelete}
          />
        ))}
      </div>
    </div>
  );
};

const PropertyCard = ({ property, onToggleFavorite, onDelete }) => {
  const getTypeIcon = () => {
    if (property.property_type === 'Residential') return <Home size={20} />;
    if (property.property_type === 'Commercial') return <TrendingUp size={20} />;
    return <MapPin size={20} />;
  };

  const getTypeColor = () => {
    if (property.property_type === 'Residential') return '#3b82f6';
    if (property.property_type === 'Commercial') return '#8b5cf6';
    return '#10b981';
  };

  return (
    <div className="property-card">
      <div className="card-actions">
        <button
          className={`favorite-button ${property.is_favorite ? 'active' : ''}`}
          onClick={() => onToggleFavorite(property.id)}
        >
          <Star size={18} fill={property.is_favorite ? '#fbbf24' : 'none'} />
        </button>
        <button
          className="delete-button"
          onClick={() => onDelete(property.id)}
        >
          <Trash2 size={16} />
        </button>
      </div>

      <div className="card-header">
        <div 
          className="property-type-badge"
          style={{ backgroundColor: getTypeColor() }}
        >
          {getTypeIcon()}
          {property.bhk || property.property_type}
        </div>
        {property.transaction_type && (
          <span className="transaction-badge">
            {property.transaction_type}
          </span>
        )}
      </div>

      <div className="card-body">
        {property.location && (
          <div className="info-row">
            <MapPin size={16} />
            <span>{property.location}</span>
          </div>
        )}

        {property.price && (
          <div className="price-tag">
            {property.price}
          </div>
        )}

        {property.carpet_area && (
          <div className="info-item">
            <strong>Area:</strong> {property.carpet_area}
          </div>
        )}

        {property.furnishing && (
          <div className="info-item">
            <strong>Furnishing:</strong> {property.furnishing}
          </div>
        )}

        {property.contact_number && (
          <div className="contact-row">
            <Phone size={16} />
            <a href={`tel:${property.contact_number}`}>
              {property.contact_number}
            </a>
          </div>
        )}

        {property.notes && (
          <div className="notes">
            {property.notes.substring(0, 100)}
            {property.notes.length > 100 && '...'}
          </div>
        )}
      </div>

      {property.tags && property.tags.length > 0 && (
        <div className="card-tags">
          {property.tags.map((tag, idx) => (
            <span key={idx} className="tag">{tag}</span>
          ))}
        </div>
      )}
    </div>
  );
};

export default PropertyList;
