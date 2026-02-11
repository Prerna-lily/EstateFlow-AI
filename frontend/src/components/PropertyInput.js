import React, { useState } from 'react';
import { MessageSquare, Sparkles, Save, Edit2, AlertCircle } from 'lucide-react';
import { propertyService } from '../services/api';
import ImageUpload from './ImageUpload';

const PropertyInput = ({ onPropertySaved }) => {
  const [message, setMessage] = useState('');
  const [extractedData, setExtractedData] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [savedPropertyId, setSavedPropertyId] = useState(null);
  const [tempImage, setTempImage] = useState(null);

  const handleExtract = async () => {
    if (!message.trim()) return;

    try {
      setIsExtracting(true);
      setError(null);
      const data = await propertyService.extractProperty(message);
      setExtractedData(data);
    } catch (err) {
      setError('Failed to extract property details. Please try again.');
      console.error(err);
    } finally {
      setIsExtracting(false);
    }
  };

  const handleSave = async () => {
    if (!extractedData) return;

    try {
      setIsSaving(true);
      setError(null);
      const response = await propertyService.saveProperty(extractedData);
      setSavedPropertyId(response.id);
      
      // If temp image exists, upload it
      if (tempImage) {
        const fileInput = document.getElementById('temp-image-input');
        if (fileInput && fileInput.files.length > 0) {
          const formData = new FormData();
          formData.append('file', fileInput.files[0]);
          
          try {
            await fetch(`http://localhost:8000/api/upload-image/${response.id}`, {
              method: 'POST',
              body: formData,
            });
          } catch (imgErr) {
            console.error('Image upload after save failed:', imgErr);
          }
        }
      }
      
      setSuccess(true);
      setMessage('');
      
      if (onPropertySaved) {
        onPropertySaved();
      }

      setTimeout(() => {
        setSuccess(false);
        setExtractedData(null);
        setTempImage(null);
      }, 2000);
    } catch (err) {
      if (err.response?.status === 409) {
        setError('Duplicate property detected! This property might already exist.');
      } else {
        setError('Failed to save property. Please try again.');
      }
      console.error(err);
    } finally {
      setIsSaving(false);
    }
  };

  const handleFieldChange = (field, value) => {
    setExtractedData({
      ...extractedData,
      [field]: value
    });
  };

  const getConfidenceColor = (score) => {
    if (score >= 70) return '#10b981';
    if (score >= 40) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="property-input">
      <div className="input-card">
        <div className="card-header">
          <MessageSquare className="header-icon" />
          <h2>Add Property</h2>
        </div>

        {/* Image Upload Section - Shown First */}
        <div className="image-upload-top">
          <h3>📸 Upload Property Image (Optional)</h3>
          <div className="upload-input-wrapper">
            <input
              id="temp-image-input"
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files[0];
                if (file) {
                  const reader = new FileReader();
                  reader.onload = (event) => {
                    setTempImage(event.target.result);
                  };
                  reader.readAsDataURL(file);
                }
              }}
              className="image-input"
            />
            <label htmlFor="temp-image-input" className="image-input-label-top">
              📁 Choose Image (Max 5MB)
            </label>
          </div>
          {tempImage && (
            <div className="temp-image-preview">
              <img src={tempImage} alt="Preview" className="temp-preview-img" />
              <small>Image will be uploaded with property</small>
            </div>
          )}
        </div>

        <div className="message-input-section">
          <label>WhatsApp Message</label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Paste WhatsApp message here...&#10;Example: 2BHK for rent in Borivali West, 850 sqft, semi-furnished, 35000/month. Contact 9876543210"
            rows={6}
            className="message-textarea"
          />
          
          <button
            onClick={handleExtract}
            disabled={!message.trim() || isExtracting}
            className="extract-button"
          >
            <Sparkles size={18} />
            {isExtracting ? 'Extracting...' : 'Extract with AI'}
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            ✓ Property saved successfully!
          </div>
        )}

        {extractedData && (
          <div className="extracted-data">
            <div className="extracted-header">
              <h3>
                <Edit2 size={18} />
                Extracted Details
              </h3>
              <div 
                className="confidence-badge"
                style={{ 
                  backgroundColor: getConfidenceColor(extractedData.confidence_score) 
                }}
              >
                {extractedData.confidence_score}% Confidence
              </div>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label>Property Type</label>
                <select
                  value={extractedData.property_type || ''}
                  onChange={(e) => handleFieldChange('property_type', e.target.value)}
                >
                  <option value="">Select Type</option>
                  <option value="Residential">Residential</option>
                  <option value="Commercial">Commercial</option>
                  <option value="Land">Land</option>
                </select>
              </div>

              <div className="form-group">
                <label>BHK / Type</label>
                <input
                  type="text"
                  value={extractedData.bhk || ''}
                  onChange={(e) => handleFieldChange('bhk', e.target.value)}
                  placeholder="e.g., 2BHK, Shop"
                />
              </div>

              <div className="form-group">
                <label>Transaction</label>
                <select
                  value={extractedData.transaction_type || ''}
                  onChange={(e) => handleFieldChange('transaction_type', e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="Rent">Rent</option>
                  <option value="Sale">Sale</option>
                </select>
              </div>

              <div className="form-group">
                <label>Location</label>
                <input
                  type="text"
                  value={extractedData.location || ''}
                  onChange={(e) => handleFieldChange('location', e.target.value)}
                  placeholder="Area name"
                />
              </div>

              <div className="form-group">
                <label>Price</label>
                <input
                  type="text"
                  value={extractedData.price || ''}
                  onChange={(e) => handleFieldChange('price', e.target.value)}
                  placeholder="₹ 35,000"
                />
              </div>

              <div className="form-group">
                <label>Carpet Area</label>
                <input
                  type="text"
                  value={extractedData.carpet_area || ''}
                  onChange={(e) => handleFieldChange('carpet_area', e.target.value)}
                  placeholder="850 sqft"
                />
              </div>

              <div className="form-group">
                <label>Contact Number</label>
                <input
                  type="text"
                  value={extractedData.contact_number || ''}
                  onChange={(e) => handleFieldChange('contact_number', e.target.value)}
                  placeholder="9876543210"
                />
              </div>

              <div className="form-group">
                <label>Furnishing</label>
                <select
                  value={extractedData.furnishing || ''}
                  onChange={(e) => handleFieldChange('furnishing', e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="Furnished">Furnished</option>
                  <option value="Semi-Furnished">Semi-Furnished</option>
                  <option value="Unfurnished">Unfurnished</option>
                </select>
              </div>
            </div>

            <div className="form-group full-width">
              <label>Notes</label>
              <textarea
                value={extractedData.notes || ''}
                onChange={(e) => handleFieldChange('notes', e.target.value)}
                rows={3}
                placeholder="Additional notes..."
              />
            </div>

            <button
              onClick={handleSave}
              disabled={isSaving || savedPropertyId}
              className="save-button"
            >
              <Save size={18} />
              {isSaving ? 'Saving...' : savedPropertyId ? '✓ Saved' : 'Save Property'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PropertyInput;
