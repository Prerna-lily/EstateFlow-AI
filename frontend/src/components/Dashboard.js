import React from 'react';
import { TrendingUp, Home, DollarSign, Star, Calendar } from 'lucide-react';

const Dashboard = ({ stats, loading }) => {
  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="empty-state">
        <TrendingUp size={48} />
        <h3>No Data Available</h3>
        <p>Add some properties to see statistics</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>

      <div className="stats-grid">
        <StatCard
          icon={<Home size={24} />}
          title="Total Properties"
          value={stats.total_properties}
          color="#3b82f6"
        />
        <StatCard
          icon={<Star size={24} />}
          title="Favorites"
          value={stats.favorites}
          color="#fbbf24"
        />
        <StatCard
          icon={<DollarSign size={24} />}
          title="For Rent"
          value={stats.by_transaction?.Rent || 0}
          color="#10b981"
        />
        <StatCard
          icon={<TrendingUp size={24} />}
          title="For Sale"
          value={stats.by_transaction?.Sale || 0}
          color="#8b5cf6"
        />
      </div>

      <div className="dashboard-section">
        <h3>By Property Type</h3>
        <div className="chart-bars">
          {Object.entries(stats.by_type || {}).map(([type, count]) => (
            <div key={type} className="bar-item">
              <div className="bar-label">{type}</div>
              <div className="bar-container">
                <div
                  className="bar-fill"
                  style={{
                    width: `${(count / stats.total_properties) * 100}%`,
                    backgroundColor: getTypeColor(type)
                  }}
                >
                  <span className="bar-value">{count}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="dashboard-section">
        <h3>
          <Calendar size={20} />
          Recent Properties
        </h3>
        <div className="recent-list">
          {stats.recent?.map((property) => (
            <div key={property.id} className="recent-item">
              <div className="recent-info">
                <strong>{property.bhk || property.property_type}</strong>
                <span>{property.location || 'No location'}</span>
              </div>
              <div className="recent-meta">
                <span className="recent-price">{property.price || 'N/A'}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, color }) => {
  return (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <div className="stat-icon" style={{ color }}>
        {icon}
      </div>
      <div className="stat-content">
        <div className="stat-title">{title}</div>
        <div className="stat-value">{value}</div>
      </div>
    </div>
  );
};

const getTypeColor = (type) => {
  if (type === 'Residential') return '#3b82f6';
  if (type === 'Commercial') return '#8b5cf6';
  if (type === 'Land') return '#10b981';
  return '#6b7280';
};

export default Dashboard;
