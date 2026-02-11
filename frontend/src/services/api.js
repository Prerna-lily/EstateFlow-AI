import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const propertyService = {
  // Extract property details from message
  extractProperty: async (message) => {
    const response = await api.post('/api/extract', { message });
    return response.data;
  },

  // Save property
  saveProperty: async (propertyData) => {
    const response = await api.post('/api/properties', propertyData);
    return response.data;
  },

  // Get all properties with filters
  getProperties: async (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        params.append(key, filters[key]);
      }
    });
    const response = await api.get(`/api/properties?${params.toString()}`);
    return response.data;
  },

  // Get single property
  getProperty: async (id) => {
    const response = await api.get(`/api/properties/${id}`);
    return response.data;
  },

  // Update property
  updateProperty: async (id, propertyData) => {
    const response = await api.put(`/api/properties/${id}`, propertyData);
    return response.data;
  },

  // Delete property
  deleteProperty: async (id) => {
    const response = await api.delete(`/api/properties/${id}`);
    return response.data;
  },

  // Toggle favorite
  toggleFavorite: async (id) => {
    const response = await api.patch(`/api/properties/${id}/favorite`);
    return response.data;
  },

  // Update tags
  updateTags: async (id, tags) => {
    const response = await api.patch(`/api/properties/${id}/tags`, tags);
    return response.data;
  },

  // Get statistics
  getStats: async () => {
    const response = await api.get('/api/stats');
    return response.data;
  },
};

export default api;
