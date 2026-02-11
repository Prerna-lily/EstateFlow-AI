"""
AI Property Extraction Module
This module uses pattern matching and NLP techniques to extract property details
from unstructured WhatsApp messages.
"""

import re
from typing import Dict, Optional, List, Tuple


class PropertyExtractor:
    """Main class for extracting property information from text"""
    
    def __init__(self):
        # Property type patterns
        self.property_patterns = {
            'residential': {
                '1BHK': r'\b1\s*bhk\b|\b1\s*rk\b|\bone\s*bhk\b',
                '2BHK': r'\b2\s*bhk\b|\btwo\s*bhk\b',
                '3BHK': r'\b3\s*bhk\b|\bthree\s*bhk\b',
                '4BHK': r'\b4\s*bhk\b|\bfour\s*bhk\b',
                '5BHK': r'\b5\s*bhk\b|\bfive\s*bhk\b',
            },
            'commercial': {
                'Shop': r'\bshop\b|\bshops\b|\bdukan\b',
                'Office': r'\boffice\b|\bcommercial\s*space\b',
                'Showroom': r'\bshowroom\b',
                'Warehouse': r'\bwarehouse\b|\bgodown\b',
            },
            'land': {
                'Residential Land': r'\bresidential\s*land\b|\bplot\b|\bploat\b',
                'Commercial Land': r'\bcommercial\s*land\b',
            }
        }
        
        # Transaction type patterns
        self.transaction_patterns = {
            'Rent': r'\brent\b|\blease\b|\brentals\b|\bkiraya\b|\bto\s*let\b',
            'Sale': r'\bsale\b|\bsell\b|\boutright\b|\bfor\s*sale\b|\bbuy\b|\bpurchase\b',
        }
        
        # Mumbai areas (Western, Central, Harbour lines)
        self.mumbai_areas = {
            'Western': [
                'Churchgate', 'Marine Lines', 'Charni Road', 'Grant Road', 'Mumbai Central',
                'Mahalaxmi', 'Lower Parel', 'Prabhadevi', 'Dadar', 'Matunga Road',
                'Mahim', 'Bandra', 'Khar Road', 'Santacruz', 'Vile Parle',
                'Andheri', 'Jogeshwari', 'Goregaon', 'Malad', 'Kandivali',
                'Borivali', 'Dahisar', 'Mira Road', 'Bhayandar', 'Naigaon',
                'Vasai', 'Nallasopara', 'Virar'
            ],
            'Central': [
                'CSMT', 'Masjid', 'Sandhurst Road', 'Byculla', 'Chinchpokli',
                'Currey Road', 'Parel', 'Dadar', 'Matunga', 'Sion',
                'Kurla', 'Vidyavihar', 'Ghatkopar', 'Vikhroli', 'Kanjurmarg',
                'Bhandup', 'Nahur', 'Mulund', 'Thane', 'Kalwa',
                'Mumbra', 'Diva', 'Kopar', 'Dombivli', 'Thakurli',
                'Kalyan', 'Ulhasnagar', 'Ambivli', 'Titwala', 'Khadavli',
                'Vasind', 'Asangaon', 'Atgaon', 'Khardi', 'Kasara'
            ],
            'Harbour': [
                'CSMT', 'Vadala Road', 'GTB Nagar', 'Chunabhatti', 'Kurla',
                'Tilak Nagar', 'Chembur', 'Govandi', 'Mankhurd', 'Vashi',
                'Sanpada', 'Juinagar', 'Nerul', 'Seawoods', 'Belapur',
                'Kharghar', 'Mansarovar', 'Khandeshwar', 'Panvel'
            ]
        }
        
        # Furnishing patterns
        self.furnishing_patterns = {
            'Furnished': r'\bfurnished\b|\bfully\s*furnished\b',
            'Semi-Furnished': r'\bsemi\s*furnished\b|\bsemi\b',
            'Unfurnished': r'\bunfurnished\b|\bbare\b',
        }
    
    def extract_property_details(self, message: str) -> Dict:
        """
        Main extraction method that processes the message and extracts all details
        """
        message_lower = message.lower()
        
        extracted = {
            'property_type': None,
            'bhk': None,
            'transaction_type': None,
            'location': None,
            'area': None,
            'region': None,
            'price': None,
            'carpet_area': None,
            'furnishing': None,
            'floor': None,
            'building_name': None,
            'owner_name': None,
            'contact_number': None,
            'availability': None,
            'notes': message,
            'raw_message': message,
            'confidence_score': 0.0
        }
        
        confidence_points = 0
        max_points = 8
        
        # Extract property type and BHK
        prop_type, bhk = self._extract_property_type(message_lower)
        if prop_type:
            extracted['property_type'] = prop_type
            extracted['bhk'] = bhk
            confidence_points += 2
        
        # Extract transaction type
        transaction = self._extract_transaction_type(message_lower)
        if transaction:
            extracted['transaction_type'] = transaction
            confidence_points += 1
        
        # Extract location
        location, area, region = self._extract_location(message)
        if location:
            extracted['location'] = location
            extracted['area'] = area
            extracted['region'] = region
            confidence_points += 2
        
        # Extract price
        price = self._extract_price(message)
        if price:
            extracted['price'] = price
            confidence_points += 1
        
        # Extract carpet area
        carpet_area = self._extract_carpet_area(message)
        if carpet_area:
            extracted['carpet_area'] = carpet_area
            confidence_points += 0.5
        
        # Extract contact number
        contact = self._extract_contact(message)
        if contact:
            extracted['contact_number'] = contact
            confidence_points += 1
        
        # Extract furnishing
        furnishing = self._extract_furnishing(message_lower)
        if furnishing:
            extracted['furnishing'] = furnishing
            confidence_points += 0.5
        
        # Calculate confidence score
        extracted['confidence_score'] = round((confidence_points / max_points) * 100, 2)
        
        return extracted
    
    def _extract_property_type(self, message: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract property type and BHK configuration"""
        # Check residential first
        for bhk, pattern in self.property_patterns['residential'].items():
            if re.search(pattern, message, re.IGNORECASE):
                return ('Residential', bhk)
        
        # Check commercial
        for prop_type, pattern in self.property_patterns['commercial'].items():
            if re.search(pattern, message, re.IGNORECASE):
                return ('Commercial', prop_type)
        
        # Check land
        for land_type, pattern in self.property_patterns['land'].items():
            if re.search(pattern, message, re.IGNORECASE):
                return ('Land', land_type)
        
        return (None, None)
    
    def _extract_transaction_type(self, message: str) -> Optional[str]:
        """Extract whether it's for rent or sale"""
        for trans_type, pattern in self.transaction_patterns.items():
            if re.search(pattern, message, re.IGNORECASE):
                return trans_type
        return None
    
    def _extract_location(self, message: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract location from Mumbai areas"""
        message_lower = message.lower()
        
        for region, areas in self.mumbai_areas.items():
            for area in areas:
                if area.lower() in message_lower:
                    return (area, area, region)
        
        # Try to extract generic location patterns
        location_patterns = [
            r'(?:at|in|near|@)\s+([A-Za-z\s]+?)(?:,|\.|$)',
            r'location[:\s]+([A-Za-z\s]+?)(?:,|\.|$)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                return (location, location, None)
        
        return (None, None, None)
    
    def _extract_price(self, message: str) -> Optional[str]:
        """Extract price or rent amount"""
        # Patterns for Indian currency
        patterns = [
            r'₹\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lac|lakh|lakhs|cr|crore|crores|k|thousand)?',
            r'rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lac|lakh|lakhs|cr|crore|crores|k|thousand)?',
            r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lac|lakh|lakhs|cr|crore|crores|k|thousand)',
            r'price[:\s]+(?:₹|rs\.?)?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'rent[:\s]+(?:₹|rs\.?)?\s*(\d+(?:,\d+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_carpet_area(self, message: str) -> Optional[str]:
        """Extract carpet area in sq ft"""
        patterns = [
            r'(\d+(?:,\d+)?)\s*(?:sq\.?\s*ft|sqft|square\s*feet)',
            r'carpet\s*area[:\s]+(\d+(?:,\d+)?)',
            r'area[:\s]+(\d+(?:,\d+)?)\s*(?:sq\.?\s*ft|sqft)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_contact(self, message: str) -> Optional[str]:
        """Extract Indian phone numbers"""
        patterns = [
            r'\+91[\s-]?\d{10}',
            r'\b[6-9]\d{9}\b',
            r'\b\d{5}[\s-]?\d{5}\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_furnishing(self, message: str) -> Optional[str]:
        """Extract furnishing status"""
        for furn_type, pattern in self.furnishing_patterns.items():
            if re.search(pattern, message, re.IGNORECASE):
                return furn_type
        return None
    
    def detect_duplicate(self, new_property: Dict, existing_properties: List[Dict]) -> Optional[Dict]:
        """
        Detect if a property already exists based on phone number and text similarity
        """
        new_contact = new_property.get('contact_number')
        new_message = new_property.get('raw_message', '').lower()
        
        if not new_contact:
            return None
        
        for existing in existing_properties:
            existing_contact = existing.get('contact_number')
            
            # Check if phone numbers match
            if existing_contact and new_contact in existing_contact:
                # Calculate text similarity (simple word overlap)
                similarity = self._calculate_text_similarity(
                    new_message, 
                    existing.get('raw_message', '').lower()
                )
                
                if similarity > 0.6:  # 60% similarity threshold
                    return existing
        
        return None
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity based on word overlap"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)


# Global extractor instance
extractor = PropertyExtractor()
