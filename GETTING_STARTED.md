# Getting Started Guide

## Welcome! 👋

This guide will help you get the Real Estate AI application up and running in minutes.

## What You'll Build

A complete property management system with:
- AI-powered property extraction from WhatsApp messages
- Smart search and filtering
- Dashboard with statistics
- Beautiful, responsive UI

## Prerequisites

Before starting, make sure you have:

1. **Python 3.8 or higher**
   - Check: `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Node.js 14 or higher**
   - Check: `node --version`
   - Download: https://nodejs.org/

3. **Git** (optional, for cloning)
   - Check: `git --version`

## Installation Steps

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to project directory
cd real-estate-ai

# Run setup script
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### Step 1: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test AI extraction
python test_extraction.py
```

#### Step 2: Setup Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file (optional)
cp .env.example .env
```

## Running the Application

You'll need TWO terminal windows:

### Terminal 1: Backend Server

```bash
cd backend
source venv/bin/activate  # Skip if using Windows
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Frontend Server

```bash
cd frontend
npm start
```

The browser should automatically open to `http://localhost:3000`

## First Steps After Installation

### 1. Test AI Extraction

Try adding your first property:

**Sample Message:**
```
2BHK for rent in Borivali West
850 sqft, semi-furnished
35000 per month
Contact: 9876543210
```

Steps:
1. Click "Add Property" tab
2. Paste the message
3. Click "Extract with AI"
4. Review the extracted details
5. Click "Save Property"

### 2. Search Properties

1. Click "Search" tab
2. Use filters to find properties
3. Try different combinations

### 3. View Dashboard

1. Click "Dashboard" tab
2. See statistics and recent properties

## Understanding the AI

### What Gets Extracted

The AI automatically detects:
- ✅ Property type (Residential/Commercial/Land)
- ✅ BHK configuration (1BHK, 2BHK, etc.)
- ✅ Transaction type (Rent/Sale)
- ✅ Location (60+ Mumbai areas)
- ✅ Price/Rent amount
- ✅ Carpet area (sq ft)
- ✅ Contact numbers
- ✅ Furnishing status

### Confidence Score

Each extraction gets a confidence score:
- **70-100%**: Excellent - Most fields detected
- **40-69%**: Good - Review recommended
- **0-39%**: Poor - Manual editing needed

### Supported Formats

The AI understands:
- English messages
- Hinglish (Hindi + English)
- Messages with emojis
- Multiple formats of phone numbers
- Various price formats (₹, lakhs, crores)

## API Testing

Test the backend API directly:

```bash
# Health check
curl http://localhost:8000/health

# Extract property
curl -X POST http://localhost:8000/api/extract \
  -H "Content-Type: application/json" \
  -d '{"message": "2BHK for rent in Andheri, 40000/month"}'

# Get all properties
curl http://localhost:8000/api/properties
```

## Troubleshooting

### Backend Issues

**Problem: Port 8000 already in use**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in main.py
```

**Problem: Module not found**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: Import errors**
```bash
# Ensure you're in the backend directory
cd backend
python main.py
```

### Frontend Issues

**Problem: Dependencies not installing**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem: Can't connect to API**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify API URL in .env file

**Problem: Blank page**
```bash
# Check for JavaScript errors in browser console (F12)
# Ensure all components are imported correctly
```

## Next Steps

### Customize the AI

Edit `backend/ai_extractor.py` to:
- Add new locations
- Modify extraction patterns
- Adjust confidence scoring
- Add new property types

### Enhance the UI

Edit `frontend/src/styles/App.css` to:
- Change colors and themes
- Modify layouts
- Add new styles

### Add Features

Ideas for expansion:
1. Database integration (MongoDB/PostgreSQL)
2. User authentication
3. WhatsApp bot integration
4. Image upload and OCR
5. Export to PDF/Excel
6. Client CRM

## Development Tips

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# View API docs
# Open http://localhost:8000/docs
```

### Frontend Development

```bash
# Build for production
npm run build

# The build folder is ready to deploy
```

### Code Organization

Backend:
- `main.py` - API routes and endpoints
- `ai_extractor.py` - AI extraction logic
- Add new files for database, auth, etc.

Frontend:
- `src/components/` - React components
- `src/services/` - API calls
- `src/styles/` - CSS files

## Production Deployment

### Backend (Example: Heroku)

```bash
# Add Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Deploy
heroku create your-app-name
git push heroku main
```

### Frontend (Example: Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review API endpoints in backend [README.md](backend/README.md)
- Test AI extraction with `test_extraction.py`
- Check browser console for errors (F12)

## What's Next?

Now that you have the basic app running, you can:

1. **Understand the AI**: Read through `ai_extractor.py` to see how extraction works
2. **Modify for Your Needs**: Customize locations, property types, UI
3. **Add Database**: Replace in-memory storage with MongoDB or PostgreSQL
4. **Deploy**: Put your app online for real use
5. **Extend**: Add client management, WhatsApp integration, etc.

---

**Happy Building! 🚀**

If you get stuck, don't hesitate to check the documentation or raise an issue.
