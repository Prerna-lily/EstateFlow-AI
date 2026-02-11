"""
Test script to demonstrate AI property extraction
Run this to see how the AI extracts property details
"""

from ai_extractor import extractor
import json

# Test messages
test_messages = [
    # Residential - Rent
    """
    2BHK for rent in Borivali West
    850 sqft, semi-furnished
    35000 per month
    Contact: 9876543210
    """,
    
    # Residential - Sale
    """
    3BHK flat for sale in Andheri East
    1200 sq ft carpet area
    Fully furnished, 5th floor
    Price: 1.5 Cr
    Call 9988776655
    """,
    
    # Commercial
    """
    Shop available for rent
    Location: Malad West, near station
    Area: 500 sqft
    Rent: 50,000/month
    Contact: 8877665544
    """,
    
    # Hinglish mixed
    """
    1 BHK flat rent pe chahiye
    Kandivali area mein
    Budget 25k tak
    Contact karo 7766554433
    """,
    
    # Complex message
    """
    🏠 PREMIUM 4BHK APARTMENT
    📍 Location: Bandra West
    📐 Carpet: 2000 sqft
    💰 Sale Price: ₹5.5 Crores
    🛋️ Fully Furnished
    📞 Contact: +91 9876543210
    Available immediately
    """
]

def test_extraction():
    print("=" * 80)
    print("REAL ESTATE AI - PROPERTY EXTRACTION TEST")
    print("=" * 80)
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}")
        print(f"{'='*80}")
        print("\n📱 Input Message:")
        print("-" * 80)
        print(message.strip())
        print("-" * 80)
        
        # Extract property details
        result = extractor.extract_property_details(message)
        
        print("\n🤖 AI Extracted Details:")
        print("-" * 80)
        print(f"Property Type:    {result['property_type']}")
        print(f"BHK/Type:         {result['bhk']}")
        print(f"Transaction:      {result['transaction_type']}")
        print(f"Location:         {result['location']}")
        print(f"Area:             {result['area']}")
        print(f"Region:           {result['region']}")
        print(f"Price:            {result['price']}")
        print(f"Carpet Area:      {result['carpet_area']}")
        print(f"Furnishing:       {result['furnishing']}")
        print(f"Contact:          {result['contact_number']}")
        print(f"Confidence:       {result['confidence_score']}%")
        print("-" * 80)
        
        # Confidence indicator
        score = result['confidence_score']
        if score >= 70:
            quality = "✅ EXCELLENT"
        elif score >= 50:
            quality = "⚠️  GOOD (Review recommended)"
        else:
            quality = "❌ POOR (Manual editing required)"
        
        print(f"\nExtraction Quality: {quality}")
        print()

if __name__ == "__main__":
    test_extraction()
    
    print("\n" + "=" * 80)
    print("Test complete! Start the FastAPI server to use the full application.")
    print("=" * 80)
