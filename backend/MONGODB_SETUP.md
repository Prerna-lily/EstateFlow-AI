# MongoDB Setup Guide

## Quick Start

### 1. Install MongoDB
**Windows:**
- Download from https://www.mongodb.com/try/download/community
- Run the installer and follow the setup
- MongoDB runs as a service by default

**Alternative: Using MongoDB Atlas (Cloud)**
- Create account at https://www.mongodb.com/cloud/atlas
- Create a cluster and get connection string
- Update `.env` with the connection string

### 2. Update Environment Variables

Your `.env` file already has MongoDB URI. Update it based on your setup:

**Local MongoDB:**
```
MONGODB_URI=mongodb://localhost:27017/real_estate
```

**MongoDB Atlas (Cloud):**
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/real_estate
```

### 3. Verify Connection

Run the backend and check the logs:
```bash
python main.py
```

You should see:
```
✓ MongoDB connected successfully
```

## How Data is Stored

### Properties Collection
Properties are stored in MongoDB with the following structure:
```json
{
  "_id": "ObjectId",
  "property_type": "string",
  "bhk": "string",
  "transaction_type": "Rent or Sale",
  "location": "string",
  "area": "string",
  "price": "string",
  "contact_number": "string",
  "owner_name": "string",
  "raw_message": "string",
  "is_favorite": boolean,
  "tags": ["array", "of", "tags"],
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp"
}
```

## API Endpoints

### Store a Property
```bash
POST /api/properties
Content-Type: application/json

{
  "property_type": "Apartment",
  "bhk": "2BHK",
  "transaction_type": "Rent",
  "location": "Mumbai",
  "area": "1000 sqft",
  "price": "50000",
  "raw_message": "Original message text",
  "owner_name": "John",
  "contact_number": "9876543210"
}
```

### Get All Properties
```bash
GET /api/properties
```

### Get Single Property
```bash
GET /api/properties/{property_id}
```

### Update Property
```bash
PUT /api/properties/{property_id}
```

### Delete Property
```bash
DELETE /api/properties/{property_id}
```

### Get Statistics
```bash
GET /api/stats
```

## Files Updated
- `.env` - Local environment configuration
- `.env.example` - Example environment file
- `database.py` - New MongoDB connection and CRUD operations
- `main.py` - Updated to use MongoDB instead of in-memory storage
