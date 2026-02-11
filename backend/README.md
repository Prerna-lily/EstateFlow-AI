# Real Estate AI - Backend

## Overview
FastAPI backend with AI-powered property extraction from WhatsApp messages.

## Features
- 🤖 AI Property Extraction (NLP-based)
- 🔍 Smart Search & Filters
- 📱 Contact Number Detection
- 💰 Price Extraction
- 📍 Location Detection (Mumbai areas)
- 🏠 Property Type Classification
- ⚡ Duplicate Detection
- ⭐ Favorites & Tags

## Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python main.py
```

Or using uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Property Extraction
- `POST /api/extract` - Extract property details from message
  ```json
  {
    "message": "2BHK for rent in Borivali, 25000 per month, contact 9876543210"
  }
  ```

### Property Management
- `POST /api/properties` - Save property
- `GET /api/properties` - Get all properties (with filters)
- `GET /api/properties/{id}` - Get single property
- `PUT /api/properties/{id}` - Update property
- `DELETE /api/properties/{id}` - Delete property

### Filters (Query Parameters)
- `property_type`: Residential, Commercial, Land
- `transaction_type`: Rent, Sale
- `bhk`: 1BHK, 2BHK, 3BHK, etc.
- `location`: Area name
- `search`: Keyword search

### Additional
- `PATCH /api/properties/{id}/favorite` - Toggle favorite
- `PATCH /api/properties/{id}/tags` - Update tags
- `GET /api/stats` - Get statistics

## AI Extraction Logic

The AI extractor uses pattern matching and NLP to extract:
1. **Property Type**: Residential (BHK), Commercial (Shop/Office), Land
2. **Transaction Type**: Rent or Sale
3. **Location**: Mumbai areas (Western/Central/Harbour lines)
4. **Price**: Indian currency formats (₹, lakhs, crores)
5. **Carpet Area**: Square feet
6. **Contact**: Indian phone numbers
7. **Furnishing**: Furnished, Semi-Furnished, Unfurnished

### Confidence Score
Each extraction gets a confidence score (0-100%) based on:
- Number of fields successfully extracted
- Pattern match quality

## Testing

Test the API using curl:
```bash
# Extract property details
curl -X POST http://localhost:8000/api/extract \
  -H "Content-Type: application/json" \
  -d '{"message": "2BHK for rent in Andheri West, 35000/month, 850 sqft, semi-furnished, contact 9876543210"}'
```

## Next Steps
1. Add MongoDB for persistent storage
2. Implement user authentication
3. Add advanced NLP models (spaCy, transformers)
4. Build offline sync capability
5. Add image processing (OCR for property images)
