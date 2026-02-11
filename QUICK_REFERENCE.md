# Quick Reference - Real Estate AI

## 🚀 Quick Start Commands

### Start Backend
```bash
cd backend
python main.py
```

### Start Frontend
```bash
cd frontend
npm start
```

## 📝 Sample Property Messages

### Residential - Rent
```
2BHK for rent in Borivali West
850 sqft, semi-furnished
35000 per month
Contact: 9876543210
```

### Residential - Sale
```
3BHK flat for sale in Andheri East
1200 sq ft, fully furnished
Price: 1.5 Crores
Call 9988776655
```

### Commercial
```
Shop available for rent
Malad West, near station
Area: 500 sqft
Rent: 50,000/month
Contact: 8877665544
```

## 🔧 API Quick Reference

### Extract Property
```bash
POST /api/extract
Body: {"message": "your message"}
```

### Save Property
```bash
POST /api/properties
Body: {property details}
```

### Search Properties
```bash
GET /api/properties?property_type=Residential&transaction_type=Rent
```

### Get Statistics
```bash
GET /api/stats
```

## 🎯 AI Extraction Fields

| Field | Example | Auto-Detected |
|-------|---------|---------------|
| Property Type | Residential | ✅ |
| BHK | 2BHK | ✅ |
| Transaction | Rent/Sale | ✅ |
| Location | Borivali | ✅ |
| Price | ₹35,000 | ✅ |
| Carpet Area | 850 sqft | ✅ |
| Contact | 9876543210 | ✅ |
| Furnishing | Semi-Furnished | ✅ |

## 🌍 Supported Locations (Mumbai)

### Western Line
Churchgate, Marine Lines, Charni Road, Grant Road, Mumbai Central, Mahalaxmi, Lower Parel, Prabhadevi, Dadar, Matunga Road, Mahim, Bandra, Khar Road, Santacruz, Vile Parle, Andheri, Jogeshwari, Goregaon, Malad, Kandivali, Borivali, Dahisar, Mira Road, Bhayandar, Naigaon, Vasai, Nallasopara, Virar

### Central Line
CSMT, Masjid, Sandhurst Road, Byculla, Chinchpokli, Currey Road, Parel, Dadar, Matunga, Sion, Kurla, Vidyavihar, Ghatkopar, Vikhroli, Kanjurmarg, Bhandup, Nahur, Mulund, Thane, Kalwa, Mumbra, Diva, Kopar, Dombivli, Thakurli, Kalyan

### Harbour Line
CSMT, Vadala Road, GTB Nagar, Chunabhatti, Kurla, Tilak Nagar, Chembur, Govandi, Mankhurd, Vashi, Sanpada, Juinagar, Nerul, Seawoods, Belapur, Kharghar, Mansarovar, Khandeshwar, Panvel

## 🎨 Confidence Score Guide

| Score | Quality | Action |
|-------|---------|--------|
| 70-100% | ✅ Excellent | Ready to save |
| 40-69% | ⚠️ Good | Review recommended |
| 0-39% | ❌ Poor | Manual editing required |

## 🔥 Common Use Cases

### 1. Add Property from WhatsApp
1. Copy message from WhatsApp
2. Go to "Add Property"
3. Paste message
4. Click "Extract with AI"
5. Review and Save

### 2. Search for 2BHK Rent in Borivali
1. Go to "Search"
2. Property Type: Residential
3. Transaction: Rent
4. BHK: 2BHK
5. Location: Borivali

### 3. View All Favorites
1. Go to "Search"
2. Click star icon on properties to mark favorite
3. Filter will show favorites

### 4. Check Today's Additions
1. Go to "Dashboard"
2. View "Recent Properties" section

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Change port in main.py |
| CORS error | Check backend CORS settings |
| Dependencies error | Run `pip install -r requirements.txt` |
| Frontend blank | Check browser console (F12) |
| API not connecting | Ensure backend is running |

## 📁 Key Files to Modify

### Add New Property Types
File: `backend/ai_extractor.py`
Section: `self.property_patterns`

### Add New Locations
File: `backend/ai_extractor.py`
Section: `self.mumbai_areas`

### Change UI Colors
File: `frontend/src/styles/App.css`
Section: `.app-header` and color variables

### Add New API Endpoints
File: `backend/main.py`
Add new `@app.get()` or `@app.post()` functions

## 💡 Pro Tips

1. **Bulk Import**: Copy-paste multiple messages and process them one by one
2. **Edit Before Save**: Always review AI-extracted data
3. **Use Tags**: Mark properties as "Hot", "Urgent", "Client Ready"
4. **Favorites**: Star important properties for quick access
5. **Search by Phone**: Use phone number to find all properties from a contact
6. **Dashboard**: Check statistics daily to track your inventory

## 🔮 Future Features to Add

- [ ] WhatsApp bot integration
- [ ] Database (MongoDB/PostgreSQL)
- [ ] User authentication
- [ ] Image upload with OCR
- [ ] Client CRM
- [ ] PDF brochure generation
- [ ] Export to Excel
- [ ] Multi-language support
- [ ] Offline PWA mode
- [ ] Property recommendations

## 📞 Test Numbers Format

The AI recognizes:
- `9876543210`
- `+91 9876543210`
- `98765 43210`
- `+91-9876543210`

## 💰 Price Formats Supported

- `35000`
- `₹35,000`
- `Rs. 35000`
- `35k`
- `1.5 lakhs`
- `2 crores`
- `₹1.5Cr`

---

**Save this file for quick reference! 📌**
