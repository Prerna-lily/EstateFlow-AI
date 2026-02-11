#  EstateFlow AI  
### Real Estate AI – Property Message Management System  

A smart property management system for real estate brokers that uses AI to extract structured property details from unstructured WhatsApp messages.

---

##  Features

###  Core Features (MVP)

-  **AI Property Extraction** – Automatically extract property details from WhatsApp messages  
-  **Smart Search & Filters** – Find properties quickly with advanced filtering  
-  **Contact Detection** – Extract phone numbers automatically  
-  **Price Extraction** – Detect rent/sale prices in Indian currency formats  
-  **Location Detection** – Recognize Mumbai areas (Western, Central, Harbour lines)  
-  **Property Classification** – Auto-categorize Residential, Commercial, and Land  
-  **Duplicate Detection** – Prevent duplicate entries  
-  **Favorites & Tags** – Mark and organize important properties  
-  **Dashboard** – View statistics and insights  

---

## 🤖 AI Capabilities

The AI extraction engine can detect:

- Property Type (Residential / Commercial / Land)  
- BHK Configuration (1BHK, 2BHK, 3BHK, etc.)  
- Transaction Type (Rent / Sale)  
- Location and Area  
- Price / Rent Amount  
- Carpet Area (sq ft)  
- Contact Numbers  
- Furnishing Status  
- Confidence Score for each extraction  

---

##  Architecture

### 🔹 Backend (Python – FastAPI)

- **Framework:** FastAPI  
- **AI Engine:** Custom NLP-based property extractor  
- **Storage:** In-memory (Upgradeable to MongoDB / PostgreSQL)  
- **API Type:** RESTful endpoints  

### 🔹 Frontend (React)

- **Framework:** React 18  
- **Styling:** Custom CSS  
- **Icons:** Lucide React  
- **API Client:** Axios  

---

real-estate-ai/
│
├── backend/
│ ├── main.py # FastAPI application
│ ├── ai_extractor.py # AI extraction logic
│ ├── requirements.txt # Python dependencies
│ └── README.md
│
├── frontend/
│ ├── public/
│ │ └── index.html
│ │
│ ├── src/
│ │ ├── components/
│ │ │ ├── PropertyInput.js
│ │ │ ├── PropertyList.js
│ │ │ ├── PropertyFilters.js
│ │ │ └── Dashboard.js
│ │ │
│ │ ├── services/
│ │ │ └── api.js
│ │ │
│ │ ├── styles/
│ │ │ └── App.css
│ │ │
│ │ ├── App.js
│ │ └── index.js
│ │
│ └── package.json
│
└── README.md


---

## 🚀 Quick Start

### ✅ Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

---

### 🔹 Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py


Backend will run at:
👉 http://localhost:8000

🔹 Frontend Setup
cd frontend

# Install dependencies
npm install

# Start development server
npm start


Frontend will run at:
👉 http://localhost:3000

📝 Usage Guide
1️⃣ Add Property

Navigate to Add Property

Paste WhatsApp message

Click Extract with AI

Review extracted details

Click Save Property

Example Message
2BHK for rent in Borivali West
850 sqft, semi-furnished
35000/month
Contact: 9876543210

2️⃣ Search Properties

Use filters:

Property Type

Transaction Type (Rent/Sale)

BHK

Location

Keyword Search

View results in grid layout.
Mark favorites or delete properties.

3️⃣ Dashboard

View:

Total properties

Favorites count

Distribution by type

Recent additions

🔧 API Endpoints
🔹 Property Extraction
POST /api/extract


Body

{
  "message": "property message text"
}


Response

Extracted property details

Confidence score

🔹 Property Management
GET    /api/properties
POST   /api/properties
GET    /api/properties/{id}
PUT    /api/properties/{id}
DELETE /api/properties/{id}
PATCH  /api/properties/{id}/favorite
PATCH  /api/properties/{id}/tags
GET    /api/stats

🔹 Query Parameters (GET /api/properties)

property_type → Residential, Commercial, Land

transaction_type → Rent, Sale

bhk → 1BHK, 2BHK, 3BHK

location → Area name

search → Keyword search

🎯 AI Extraction Logic
🔍 Pattern Matching

The AI uses regex patterns to detect:

Property Type

Transaction Type

60+ Mumbai locations

Indian currency formats (₹, Lakhs, Crores)

10-digit Indian phone numbers

Carpet area in sq ft

📊 Confidence Scoring
Final Score = (Points Earned / Max Points) × 100


Helps users identify which fields require manual review.

⚡ Duplicate Detection

Phone number comparison

Text similarity calculation

Alert if >60% match found

## 📁 Project Structure

