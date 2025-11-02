"""
FastAPI ML Backend for Clazzy Fashion Recommendation
Production-ready system with:
- ResNet50 for clothing classification
- K-means clustering for color extraction
- Color theory for outfit harmony
- Deep learning embeddings for style matching
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List
import os
from pathlib import Path
import io

# Import ML modules
from ml_classifier import get_classifier
from color_analyzer import get_color_analyzer
from outfit_recommender import get_outfit_recommender

app = FastAPI(
    title="Clazzy Fashion ML API",
    version="2.0.0",
    description="Production ML system with ResNet50, K-means, and color theory"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = Path(__file__).parent.parent / "client" / "public" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Global ML model instances (lazy loading)
_classifier = None
_color_analyzer = None
_recommender = None

def get_models():
    """Initialize ML models on first request (lazy loading)"""
    global _classifier, _color_analyzer, _recommender
    
    if _classifier is None:
        print("🚀 Loading ML models (ResNet50, K-means, Color Theory)...")
        _classifier = get_classifier()
        _color_analyzer = get_color_analyzer()
        _recommender = get_outfit_recommender()
        print("✅ All ML models loaded successfully!")
    
    return _classifier, _color_analyzer, _recommender


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


@app.get('/')
async def root():
    """API health check"""
    return {
        "status": "online",
        "version": "2.0.0",
        "ml_system": "ResNet50 + K-means + Color Theory"
    }


@app.post('/predict-type')
async def predict_type(file: UploadFile = File(...)):
    """
    Predict clothing type using ResNet50 deep learning model
    
    Args:
        file: Image file to classify
    
    Returns:
        {
            "predicted_type": str (top/bottom/dress/shoes/blazer/other),
            "confidence": float (0-1),
            "colors": List[dict] (top 5 dominant colors with K-means)
        }
    """
    try:
        # Initialize models
        classifier, color_analyzer, _ = get_models()
        
        # Read file bytes
        file_bytes = await file.read()
        
        # Classify using ResNet50
        prediction = classifier.predict(file_bytes)
        
        # Log classification result
        print(f"📸 Classified image: {file.filename} → {prediction['predicted_type']} ({prediction['confidence']:.2%} confidence)")
        
        # Extract colors using K-means
        colors = color_analyzer.extract_colors(file_bytes)
        
        # Get dominant color
        dominant_color = colors[0]['hex'] if colors else '#808080'
        
        return JSONResponse({
            "predicted_type": prediction['predicted_type'],
            "confidence": round(prediction['confidence'], 3),
            "colors": colors[:5],  # Top 5 colors
            "dominant_color": dominant_color
        })
        
    except Exception as e:
        print(f"❌ Error in predict_type: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@app.post('/recommend-outfits')
async def recommend_outfits(occasion: str = Form(...), max_items: int = Form(2)):
    """
    Generate intelligent outfit recommendations using:
    - Deep learning style embeddings
    - Color harmony theory (complementary, analogous, triadic)
    - Occasion-based matching rules
    
    Args:
        occasion: Event type (casual/formal/business/party/date/sports)
        max_items: Items per outfit (default: 2)
    
    Returns:
        {
            "occasion": str,
            "recommendations": List[dict] with scored outfits,
            "total_items_analyzed": int
        }
    """
    try:
        # Initialize models
        classifier, color_analyzer, recommender = get_models()
        
        # Get all uploaded files
        uploaded_files = get_uploaded_files()
        
        if not uploaded_files:
            return JSONResponse({
                "occasion": occasion,
                "recommendations": [],
                "total_items_analyzed": 0,
                "message": "No images uploaded yet"
            })
        
        # Analyze each uploaded file
        analyzed_items = []
        type_counts = {}  # Track distribution of clothing types
        
        for file_path in uploaded_files:
            try:
                # Read file
                with open(file_path, 'rb') as f:
                    file_bytes = f.read()
                
                # Classify with ResNet50
                prediction = classifier.predict(file_bytes)
                predicted_type = prediction['predicted_type']
                
                # Track type distribution
                type_counts[predicted_type] = type_counts.get(predicted_type, 0) + 1
                
                # Extract colors with K-means
                colors = color_analyzer.extract_colors(file_bytes)
                dominant_color = colors[0]['hex'] if colors else '#808080'
                
                # Create item data
                item = {
                    'id': file_path.name,
                    'type': predicted_type,
                    'colors': colors,
                    'dominant_color': dominant_color,
                    'features': prediction['features'],  # Deep learning embeddings
                    'url': f'/uploads/{file_path.name}',
                    'confidence': prediction['confidence']
                }
                
                analyzed_items.append(item)
                print(f"✅ Analyzed {file_path.name}: {predicted_type} ({prediction['confidence']:.2%})")
                
            except Exception as e:
                print(f"⚠️ Error analyzing {file_path.name}: {str(e)}")
                continue
        
        # Log wardrobe summary
        print(f"\n👔 Wardrobe Summary:")
        for clothing_type, count in sorted(type_counts.items()):
            print(f"   - {clothing_type}: {count} item(s)")
        print()
        
        if not analyzed_items:
            return JSONResponse({
                "occasion": occasion,
                "recommendations": [],
                "total_items_analyzed": 0,
                "message": "Failed to analyze uploaded images"
            })
        
        # Generate outfit recommendations using ML
        print(f"🎯 Generating outfit recommendations for: {occasion}")
        outfits = recommender.recommend_outfits(
            clothing_items=analyzed_items,
            occasion=occasion,
            max_outfits=5,
            items_per_outfit=max_items
        )
        
        print(f"✨ Generated {len(outfits)} outfit recommendations\n")
        
        # Format response
        formatted_outfits = []
        for outfit in outfits:
            formatted_items = []
            for item in outfit['items']:
                formatted_items.append({
                    'filename': item['id'],
                    'type': item['type'],
                    'category': item['type'],
                    'color': item['dominant_color'],
                    'url': item['url']
                })
            
            formatted_outfits.append({
                'items': formatted_items,
                'score': round(outfit['score'], 3),
                'total_items': outfit['total_items']
            })
        
        return JSONResponse({
            "occasion": occasion,
            "recommendations": formatted_outfits,
            "total_items_analyzed": len(analyzed_items)
        })
        
    except Exception as e:
        print(f"❌ Error in recommend_outfits: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


if __name__ == '__main__':
    print("🚀 Starting Clazzy Fashion ML Backend...")
    print("📊 ML Models: ResNet50 + K-means + Color Theory")
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
