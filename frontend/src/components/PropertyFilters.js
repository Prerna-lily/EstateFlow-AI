import React, { useState } from 'react';
import { Search, X } from 'lucide-react';

const PropertyFilters = ({ filters, onFilterChange }) => {
  const [localFilters, setLocalFilters] = useState(filters);

  const handleChange = (key, value) => {
    const newFilters = { ...localFilters, [key]: value };
    setLocalFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    setLocalFilters({});
    onFilterChange({});
  };

  const hasActiveFilters = Object.values(localFilters).some(v => v);

  return (
    <div className="property-filters">
      <div className="filters-header">
        <h3>
          <Search size={20} />
          Search & Filter
        </h3>
        {hasActiveFilters && (
          <button onClick={clearFilters} className="clear-filters">
            <X size={16} />
            Clear All
          </button>
        )}
      </div>

      <div className="filters-grid">
        <div className="filter-group">
          <label>Property Type</label>
          <select
            value={localFilters.property_type || ''}
            onChange={(e) => handleChange('property_type', e.target.value)}
          >
            <option value="">All Types</option>
            <option value="Residential">Residential</option>
            <option value="Commercial">Commercial</option>
            <option value="Land">Land</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Transaction</label>
          <select
            value={localFilters.transaction_type || ''}
            onChange={(e) => handleChange('transaction_type', e.target.value)}
          >
            <option value="">All</option>
            <option value="Rent">Rent</option>
            <option value="Sale">Sale</option>
          </select>
        </div>

        <div className="filter-group">
          <label>BHK</label>
          <select
            value={localFilters.bhk || ''}
            onChange={(e) => handleChange('bhk', e.target.value)}
          >
            <option value="">All</option>
            <option value="1BHK">1BHK</option>
            <option value="2BHK">2BHK</option>
            <option value="3BHK">3BHK</option>
            <option value="4BHK">4BHK</option>
            <option value="Shop">Shop</option>
            <option value="Office">Office</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Location</label>
          <input
            type="text"
            value={localFilters.location || ''}
            onChange={(e) => handleChange('location', e.target.value)}
            placeholder="Enter area..."
          />
        </div>

        <div className="filter-group full-width">
          <label>Search</label>
          <input
            type="text"
            value={localFilters.search || ''}
            onChange={(e) => handleChange('search', e.target.value)}
            placeholder="Search by keyword or phone number..."
          />
        </div>
      </div>
    </div>
  );
};

export default PropertyFilters;
