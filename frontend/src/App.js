import React, { useState, useEffect } from 'react';
import { MessageSquare, Search, Home, TrendingUp, Star, Plus } from 'lucide-react';
import { propertyService } from './services/api';
import PropertyInput from './components/PropertyInput';
import PropertyList from './components/PropertyList';
import PropertyFilters from './components/PropertyFilters';
import Dashboard from './components/Dashboard';
import './styles/App.css';

function App() {
  const [activeTab, setActiveTab] = useState('input');
  const [properties, setProperties] = useState([]);
  const [stats, setStats] = useState(null);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (activeTab === 'list') {
      loadProperties();
    } else if (activeTab === 'dashboard') {
      loadStats();
    }
  }, [activeTab, filters]);

  const loadProperties = async () => {
    try {
      setLoading(true);
      const data = await propertyService.getProperties(filters);
      setProperties(data);
    } catch (error) {
      console.error('Error loading properties:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await propertyService.getStats();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePropertySaved = () => {
    if (activeTab === 'list') {
      loadProperties();
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <Home className="logo-icon" />
            <h1>Real Estate AI</h1>
          </div>
          <p className="tagline">Smart Property Management for Brokers</p>
        </div>
      </header>

      <nav className="app-nav">
        <button
          className={`nav-button ${activeTab === 'input' ? 'active' : ''}`}
          onClick={() => setActiveTab('input')}
        >
          <Plus size={20} />
          Add Property
        </button>
        <button
          className={`nav-button ${activeTab === 'list' ? 'active' : ''}`}
          onClick={() => setActiveTab('list')}
        >
          <Search size={20} />
          Search
        </button>
        <button
          className={`nav-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <TrendingUp size={20} />
          Dashboard
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'input' && (
          <PropertyInput onPropertySaved={handlePropertySaved} />
        )}
        
        {activeTab === 'list' && (
          <>
            <PropertyFilters filters={filters} onFilterChange={setFilters} />
            <PropertyList 
              properties={properties} 
              loading={loading}
              onUpdate={loadProperties}
            />
          </>
        )}
        
        {activeTab === 'dashboard' && (
          <Dashboard stats={stats} loading={loading} />
        )}
      </main>

      <footer className="app-footer">
        <p>Made with ❤️ for Real Estate Brokers</p>
      </footer>
    </div>
  );
}

export default App;
