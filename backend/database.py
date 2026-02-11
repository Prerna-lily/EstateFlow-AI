from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/real_estate")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000, connectTimeoutMS=10000)
    # Verify connection
    client.admin.command('ping')
    db = client.get_database()
    print("✓ MongoDB connected successfully")
except ServerSelectionTimeoutError:
    print("✗ MongoDB connection failed. Make sure MongoDB is running.")
    db = None
except Exception as e:
    print(f"✗ MongoDB error: {str(e)}")
    db = None


def get_database():
    """Return database instance"""
    return db


def save_property(property_data: dict):
    """Save property to MongoDB"""
    if db is None:
        raise Exception("Database not connected")
    
    property_data['created_at'] = datetime.now().isoformat()
    property_data['updated_at'] = datetime.now().isoformat()
    
    result = db.properties.insert_one(property_data)
    return str(result.inserted_id)


def get_property(property_id: str):
    """Get property by ID"""
    if db is None:
        raise Exception("Database not connected")
    
    from bson.objectid import ObjectId
    try:
        return db.properties.find_one({"_id": ObjectId(property_id)})
    except:
        return None


def get_all_properties(limit: int = 100):
    """Get all properties"""
    if db is None:
        raise Exception("Database not connected")
    
    return list(db.properties.find().limit(limit))


def update_property(property_id: str, property_data: dict):
    """Update property"""
    if db is None:
        raise Exception("Database not connected")
    
    from bson.objectid import ObjectId
    property_data['updated_at'] = datetime.now().isoformat()
    
    result = db.properties.update_one(
        {"_id": ObjectId(property_id)},
        {"$set": property_data}
    )
    return result.modified_count


def delete_property(property_id: str):
    """Delete property"""
    if db is None:
        raise Exception("Database not connected")
    
    from bson.objectid import ObjectId
    result = db.properties.delete_one({"_id": ObjectId(property_id)})
    return result.deleted_count
