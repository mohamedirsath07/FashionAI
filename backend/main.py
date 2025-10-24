from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
import uvicorn
from typing import List
import os
from pathlib import Path

app = FastAPI(title="Mock ML Backend for Fashion-Style")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to uploaded images
UPLOAD_DIR = Path(__file__).parent.parent / "client" / "public" / "uploads"

def get_uploaded_files():
    """Get all uploaded image files from the uploads directory"""
    if not UPLOAD_DIR.exists():
        return []
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    files = []
    for file in UPLOAD_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:
            # Skip mock files
            if not file.name.startswith('mock_'):
                files.append(file)
    return files

def classify_by_filename(filename: str):
    """Simple classification based on filename"""
    lower = filename.lower()
    if 'shirt' in lower or 'top' in lower or 'blouse' in lower or 't-shirt' in lower or 'tshirt' in lower:
        return 'top'
    elif 'pant' in lower or 'jean' in lower or 'trouser' in lower or 'short' in lower or 'skirt' in lower:
        return 'bottom'
    elif 'shoe' in lower or 'sneaker' in lower or 'boot' in lower:
        return 'shoes'
    elif 'dress' in lower:
        return 'dress'
    elif 'blazer' in lower or 'jacket' in lower or 'coat' in lower:
        return 'blazer'
    else:
        # Random fallback
        return random.choice(['top', 'bottom'])

def get_color_from_filename(filename: str):
    """Extract color hint from filename or return a default color"""
    colors_map = {
        'black': '#000000',
        'white': '#FFFFFF',
        'red': '#EF4444',
        'blue': '#3B82F6',
        'green': '#10B981',
        'yellow': '#F59E0B',
        'purple': '#8B5CF6',
        'pink': '#EC4899',
        'gray': '#6B7280',
        'brown': '#92400E',
        'navy': '#1E3A8A',
        'beige': '#D4A574',
        'orange': '#F97316',
    }
    
    lower = filename.lower()
    for color_name, hex_code in colors_map.items():
        if color_name in lower:
            return hex_code
    
    # Default neutral colors
    return random.choice(['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'])

@app.post('/predict-type')
async def predict_type(file: UploadFile = File(...)):
    # Simple mock: classify based on filename
    predicted = classify_by_filename(file.filename or "")
    confidence = round(random.uniform(0.75, 0.98), 2)
    return JSONResponse({"predicted_type": predicted, "confidence": confidence})

@app.post('/recommend-outfits')
async def recommend_outfits(occasion: str = Form(...), max_items: int = Form(2)):
    """Generate outfit recommendations from ACTUAL uploaded files"""
    
    # Get all uploaded files
    uploaded_files = get_uploaded_files()
    
    if not uploaded_files:
        # Fallback to empty recommendations if no files uploaded
        return JSONResponse({
            "occasion": occasion,
            "recommendations": [],
            "total_items_analyzed": 0
        })
    
    # Classify files
    tops = []
    bottoms = []
    
    for file in uploaded_files:
        file_type = classify_by_filename(file.name)
        item_data = {
            "filename": file.name,
            "type": file_type,
            "category": file_type,
            "color": get_color_from_filename(file.name),
            "url": f"/uploads/{file.name}"
        }
        
        if file_type == 'top':
            tops.append(item_data)
        elif file_type == 'bottom':
            bottoms.append(item_data)
    
    # Generate outfit combinations
    outfits = []
    
    # Create up to 3 outfit combinations
    for i in range(min(3, max(len(tops), len(bottoms)))):
        items = []
        
        # Pick a top (cycle through if we have any)
        if tops:
            items.append(tops[i % len(tops)])
        
        # Pick a bottom (cycle through if we have any)
        if bottoms:
            items.append(bottoms[i % len(bottoms)])
        
        if items:  # Only add outfit if we have at least one item
            outfits.append({
                "items": items,
                "score": round(random.uniform(0.7, 0.95), 2),
                "total_items": len(items)
            })
    
    return JSONResponse({
        "occasion": occasion,
        "recommendations": outfits,
        "total_items_analyzed": len(uploaded_files)
    })

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
