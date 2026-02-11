import os
from io import BytesIO
from PIL import Image
import base64
from datetime import datetime
import uuid

# Create uploads directory if it doesn't exist
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


def validate_image(file_content: bytes, max_size_mb: int = 5) -> tuple[bool, str]:
    """Validate image file"""
    max_size = max_size_mb * 1024 * 1024
    
    if len(file_content) > max_size:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    try:
        image = Image.open(BytesIO(file_content))
        image.verify()
        return True, "Valid"
    except Exception as e:
        return False, f"Invalid image: {str(e)}"


def create_thumbnail(image_bytes: bytes, size: tuple = (200, 200)) -> bytes:
    """Create thumbnail from image bytes"""
    try:
        image = Image.open(BytesIO(image_bytes))
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG', quality=85)
        return thumb_io.getvalue()
    except Exception as e:
        print(f"Thumbnail creation error: {str(e)}")
        return None


def save_image(file_content: bytes, filename: str) -> dict:
    """Save image and create thumbnail"""
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(filename)[1] or '.jpg'
        
        # Save original image
        original_path = os.path.join(UPLOADS_DIR, f"{file_id}{file_ext}")
        with open(original_path, 'wb') as f:
            f.write(file_content)
        
        # Create thumbnail
        thumbnail_content = create_thumbnail(file_content)
        thumbnail_path = os.path.join(UPLOADS_DIR, f"{file_id}_thumb.jpg")
        
        if thumbnail_content:
            with open(thumbnail_path, 'wb') as f:
                f.write(thumbnail_content)
        
        return {
            "success": True,
            "file_id": file_id,
            "filename": filename,
            "original_path": original_path,
            "thumbnail_path": thumbnail_path,
            "size": len(file_content),
            "uploaded_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_image_base64(file_id: str, thumbnail: bool = False) -> str:
    """Get image as base64 string"""
    try:
        suffix = "_thumb" if thumbnail else ""
        
        # Try JPEG first
        path = os.path.join(UPLOADS_DIR, f"{file_id}{suffix}.jpg")
        if not os.path.exists(path):
            # Try PNG
            path = os.path.join(UPLOADS_DIR, f"{file_id}{suffix}.png")
        
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        return None
    except Exception as e:
        print(f"Error reading image: {str(e)}")
        return None


def delete_image(file_id: str) -> bool:
    """Delete image and thumbnail"""
    try:
        for path in [
            os.path.join(UPLOADS_DIR, f"{file_id}.jpg"),
            os.path.join(UPLOADS_DIR, f"{file_id}.png"),
            os.path.join(UPLOADS_DIR, f"{file_id}_thumb.jpg"),
            os.path.join(UPLOADS_DIR, f"{file_id}_thumb.png"),
        ]:
            if os.path.exists(path):
                os.remove(path)
        return True
    except Exception as e:
        print(f"Error deleting image: {str(e)}")
        return False
