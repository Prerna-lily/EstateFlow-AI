#!/bin/bash

echo "======================================"
echo "Real Estate AI - Setup Script"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python 3 found"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi
echo "✅ Node.js found"

# Setup Backend
echo ""
echo "Setting up Backend..."
cd backend

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"

# Setup Frontend
cd ../frontend
echo ""
echo "Setting up Frontend..."
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

cd ..

echo ""
echo "======================================"
echo "Setup Complete! 🎉"
echo "======================================"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "The app will open at http://localhost:3000"
echo "API will be available at http://localhost:8000"
echo ""
