import React, { useState, useEffect } from 'react';
import '../styles/ImageUpload.css';

const ImageUpload = ({ propertyId, onUploadSuccess }) => {
  const [image, setImage] = useState(null);
  const [thumbnail, setThumbnail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [hasImage, setHasImage] = useState(false);

  // Load existing image when component mounts or propertyId changes
  useEffect(() => {
    if (propertyId) {
      loadPropertyImage();
    }
  }, [propertyId]);

  const loadPropertyImage = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/property-images/${propertyId}`);
      const data = await response.json();
      
      if (data.has_image) {
        setHasImage(true);
        setImage(data.image_base64 || data.image_url);
        setThumbnail(data.thumbnail_base64 || data.thumbnail_url);
      }
    } catch (error) {
      console.error('Error loading image:', error);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file size (5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      setMessage('❌ File size exceeds 5MB limit');
      return;
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setMessage('❌ Please select a valid image file');
      return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = (event) => {
      setImage(event.target.result);
      setMessage('');
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!image) {
      setMessage('❌ Please select an image first');
      return;
    }

    if (!propertyId) {
      setMessage('❌ Please save the property first');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      // Get the file from input
      const fileInput = document.getElementById('image-input');
      const file = fileInput.files[0];

      if (!file) {
        setMessage('❌ Please select a file');
        setLoading(false);
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(
        `http://localhost:8000/api/upload-image/${propertyId}`,
        {
          method: 'POST',
          body: formData,
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage('✅ Image uploaded successfully! Auto thumbnail created.');
        setHasImage(true);
        // Reload image to show thumbnail
        setTimeout(() => {
          loadPropertyImage();
        }, 500);
        if (onUploadSuccess) {
          onUploadSuccess(data);
        }
      } else {
        setMessage(`❌ ${data.detail || 'Upload failed'}`);
      }
    } catch (error) {
      setMessage(`❌ Error uploading image: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!propertyId) return;

    if (!window.confirm('Delete this image?')) return;

    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/property-images/${propertyId}`,
        {
          method: 'DELETE',
        }
      );

      if (response.ok) {
        setImage(null);
        setThumbnail(null);
        setHasImage(false);
        setMessage('✅ Image deleted successfully');
      } else {
        setMessage('❌ Failed to delete image');
      }
    } catch (error) {
      setMessage(`❌ Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="image-upload-container">
      <div className="image-upload-section">
        <h3>📸 Property Images</h3>
        
        <div className="upload-input-wrapper">
          <input
            id="image-input"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            disabled={loading}
            className="image-input"
          />
          <label htmlFor="image-input" className="image-input-label">
            Choose Image (Max 5MB)
          </label>
        </div>

        {image && (
          <div className="image-preview">
            {image.startsWith('data:') ? (
              <img src={image} alt="Preview" className="preview-image" />
            ) : (
              <img src={image} alt="Preview" className="preview-image" />
            )}
          </div>
        )}

        {thumbnail && (
          <div className="thumbnail-preview">
            <p className="thumbnail-label">Thumbnail Preview:</p>
            {thumbnail.startsWith('data:') ? (
              <img src={thumbnail} alt="Thumbnail" className="thumbnail-image" />
            ) : (
              <img src={thumbnail} alt="Thumbnail" className="thumbnail-image" />
            )}
          </div>
        )}

        <div className="button-group">
          <button
            onClick={handleUpload}
            disabled={!image || loading || !propertyId}
            className="btn btn-upload"
          >
            {loading ? '⏳ Uploading...' : '⬆️ Upload Image'}
          </button>

          {hasImage && (
            <button
              onClick={handleDelete}
              disabled={loading}
              className="btn btn-delete"
            >
              {loading ? '⏳ Deleting...' : '🗑️ Delete Image'}
            </button>
          )}
        </div>

        {message && (
          <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}

        <div className="info-box">
          <p>ℹ️ <strong>Max size:</strong> 5MB</p>
          <p>ℹ️ <strong>Auto thumbnails:</strong> Created automatically!</p>
          <p>ℹ️ <strong>Formats:</strong> JPG, PNG, WebP</p>
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;
