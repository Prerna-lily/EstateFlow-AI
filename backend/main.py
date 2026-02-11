from fastapi import FastAPI, HTTPException, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import re
from datetime import datetime
from ai_extractor import extractor
from database import save_property, get_property, get_all_properties, update_property, delete_property
from bson.objectid import ObjectId
from image_handler import validate_image, save_image, get_image_base64, delete_image
import os
import json


def convert_objectid(obj):
    """Recursively convert ObjectId to string in MongoDB documents"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        converted = {k: convert_objectid(v) for k, v in obj.items()}
        # Ensure id field is set from _id if present
        if '_id' in converted and 'id' not in converted:
            converted['id'] = converted['_id']
        return converted
    elif isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    return obj

app = FastAPI(title="Real Estate AI API")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for static files
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


class PropertyData(BaseModel):
    property_type: Optional[str] = None
    bhk: Optional[str] = None
    transaction_type: Optional[str] = None  # Rent or Sale
    location: Optional[str] = None
    area: Optional[str] = None
    price: Optional[str] = None
    carpet_area: Optional[str] = None
    furnishing: Optional[str] = None
    floor: Optional[str] = None
    building_name: Optional[str] = None
    owner_name: Optional[str] = None
    contact_number: Optional[str] = None
    availability: Optional[str] = None
    notes: Optional[str] = None
    raw_message: str
    confidence_score: Optional[float] = None


class PropertyResponse(BaseModel):
    id: str  # MongoDB ObjectId as string
    property_type: Optional[str]
    bhk: Optional[str]
    transaction_type: Optional[str]
    location: Optional[str]
    area: Optional[str]
    price: Optional[str]
    carpet_area: Optional[str]
    furnishing: Optional[str]
    floor: Optional[str]
    building_name: Optional[str]
    owner_name: Optional[str]
    contact_number: Optional[str]
    availability: Optional[str]
    notes: Optional[str]
    raw_message: str
    confidence_score: Optional[float]
    created_at: str
    is_favorite: bool
    tags: List[str]
    
    class Config:
        arbitrary_types_allowed = True
    price: Optional[str]
    carpet_area: Optional[str]
    furnishing: Optional[str]
    floor: Optional[str]
    building_name: Optional[str]
    owner_name: Optional[str]
    contact_number: Optional[str]
    availability: Optional[str]
    notes: Optional[str]
    raw_message: str
    confidence_score: Optional[float]
    created_at: str
    is_favorite: bool
    tags: List[str]


class MessageInput(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {
        "message": "Real Estate AI API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/extract", response_model=PropertyData)
async def extract_property(message_input: MessageInput):
    """
    Extract property details from WhatsApp message using AI
    """
    try:
        extracted_data = extractor.extract_property_details(message_input.message)
        return PropertyData(**extracted_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.post("/api/properties", response_model=dict)
async def create_property(property_data: PropertyData):
    """
    Save a property to MongoDB
    """
    try:
        property_dict = property_data.model_dump()
        property_dict['is_favorite'] = False
        property_dict['tags'] = []
        
        property_id = save_property(property_dict)
        
        return {
            "id": property_id,
            "message": "Property saved successfully"
        }
    except Exception as e:
        print(f"Error saving property: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save property: {str(e)}")


@app.get("/api/properties", response_model=List[dict])
async def get_properties_list(
    property_type: Optional[str] = Query(None),
    transaction_type: Optional[str] = Query(None),
    bhk: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """
    Get all properties from MongoDB with optional filters
    """
    try:
        properties = get_all_properties()
        
        # Apply filters
        if property_type:
            properties = [p for p in properties if p.get('property_type') == property_type]
        
        if transaction_type:
            properties = [p for p in properties if p.get('transaction_type') == transaction_type]
        
        if bhk:
            properties = [p for p in properties if p.get('bhk') == bhk]
        
        if location:
            properties = [p for p in properties 
                          if location.lower() in str(p.get('location', '')).lower()]
        
        if search:
            search_lower = search.lower()
            properties = [
                p for p in properties
                if search_lower in str(p.get('raw_message', '')).lower() or
                   search_lower in str(p.get('contact_number', '')).lower()
            ]
        
        # Convert all ObjectIds to strings and add id field from _id
        properties = [convert_objectid(p) for p in properties]
        
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/properties/{property_id}", response_model=dict)
async def get_property_by_id(property_id: str):
    """
    Get a specific property by ID from MongoDB
    """
    try:
        prop = get_property(property_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        prop = convert_objectid(prop)
        return prop
    except Exception as e:
        raise HTTPException(status_code=404, detail="Property not found")


@app.put("/api/properties/{property_id}", response_model=dict)
async def update_property_handler(property_id: str, property_data: PropertyData):
    """
    Update a property in MongoDB
    """
    try:
        update_count = update_property(property_id, {
            **property_data.model_dump(exclude_unset=True),
            "updated_at": datetime.now().isoformat()
        })
        
        if update_count == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        
        updated = get_property(property_id)
        updated['id'] = str(updated.get('_id', ''))
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/properties/{property_id}")
async def delete_property_handler(property_id: str):
    """
    Delete a property from MongoDB
    """
    try:
        delete_count = delete_property(property_id)
        
        if delete_count == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        
        return {"message": "Property deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/properties/{property_id}/favorite")
async def toggle_favorite(property_id: str):
    """
    Toggle favorite status in MongoDB
    """
    try:
        prop = get_property(property_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        new_favorite_status = not prop.get('is_favorite', False)
        update_property(property_id, {'is_favorite': new_favorite_status})
        
        return {"message": "Favorite status updated", "is_favorite": new_favorite_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/properties/{property_id}/tags")
async def update_tags(property_id: str, tags: List[str]):
    """
    Update property tags in MongoDB
    """
    try:
        prop = get_property(property_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        update_property(property_id, {'tags': tags})
        
        return {"message": "Tags updated", "tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_statistics():
    """
    Get database statistics from MongoDB
    """
    try:
        properties = get_all_properties()
        total = len(properties)
        
        # Get recent properties and convert all ObjectIds to strings
        recent_props = sorted(properties, key=lambda x: x.get('created_at', ''), reverse=True)[:5]
        recent_props = [convert_objectid(p) for p in recent_props]
        
        stats = {
            "total_properties": total,
            "by_type": {},
            "by_transaction": {},
            "favorites": len([p for p in properties if p.get('is_favorite', False)]),
            "recent": recent_props
        }
        
        # Count by property type
        for prop in properties:
            prop_type = prop.get('property_type', 'Unknown')
            stats['by_type'][prop_type] = stats['by_type'].get(prop_type, 0) + 1
        
        # Count by transaction type
        for prop in properties:
            trans_type = prop.get('transaction_type', 'Unknown')
            stats['by_transaction'][trans_type] = stats['by_transaction'].get(trans_type, 0) + 1
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== IMAGE UPLOAD ENDPOINTS ====================

@app.post("/api/upload-image/{property_id}")
async def upload_image(property_id: str, file: UploadFile = File(...)):
    """
    Upload image for a property
    """
    try:
        # Validate property exists
        prop = get_property(property_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Read file content
        content = await file.read()
        
        # Validate image
        is_valid, message = validate_image(content)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Save image and create thumbnail
        result = save_image(content, file.filename)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Update property with image info
        update_property(property_id, {
            "image_id": result["file_id"],
            "image_filename": result["filename"],
            "image_size": result["size"]
        })
        
        return {
            "success": True,
            "file_id": result["file_id"],
            "filename": result["filename"],
            "image_url": f"/uploads/{result['file_id']}.jpg",
            "thumbnail_url": f"/uploads/{result['file_id']}_thumb.jpg"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/api/property-images/{property_id}")
async def get_property_images(property_id: str):
    """
    Get images for a property
    """
    try:
        prop = get_property(property_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        if "image_id" not in prop:
            return {
                "has_image": False,
                "images": []
            }
        
        file_id = prop["image_id"]
        
        # Get image as base64
        image_b64 = get_image_base64(file_id)
        thumbnail_b64 = get_image_base64(file_id, thumbnail=True)
        
        return {
            "has_image": True,
            "file_id": file_id,
            "filename": prop.get("image_filename"),
            "image_base64": f"data:image/jpeg;base64,{image_b64}" if image_b64 else None,
            "thumbnail_base64": f"data:image/jpeg;base64,{thumbnail_b64}" if thumbnail_b64 else None,
            "image_url": f"/uploads/{file_id}.jpg",
            "thumbnail_url": f"/uploads/{file_id}_thumb.jpg"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/property-images/{property_id}")
async def delete_property_image(property_id: str):
    """
    Delete image for a property
    """
    try:
        prop = get_property(property_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        
        if "image_id" not in prop:
            raise HTTPException(status_code=404, detail="No image found for this property")
        
        file_id = prop["image_id"]
        delete_image(file_id)
        
        # Remove image info from property
        update_property(property_id, {
            "image_id": None,
            "image_filename": None,
            "image_size": None
        })
        
        return {"message": "Image deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
