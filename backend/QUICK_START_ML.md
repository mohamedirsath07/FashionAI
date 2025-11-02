# 🚀 Clazzy ML Quick Reference

## Installation

```bash
cd backend
pip install -r requirements.txt
python test_ml.py  # Verify setup
python main.py     # Start server
```

## API Usage

### Classify Image
```bash
POST http://localhost:8000/predict-type
Content-Type: multipart/form-data

file: <image>
```

### Get Recommendations
```bash
POST http://localhost:8000/recommend-outfits
Content-Type: application/x-www-form-urlencoded

occasion: casual|formal|business|party|date|sports
max_items: 2
```

## ML Models

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Classifier** | ResNet50 (ImageNet) | Clothing type detection |
| **Color Extractor** | K-means (k=5) | Dominant color analysis |
| **Harmony Engine** | Color Theory | Complementary/analogous matching |
| **Recommender** | Deep Learning + Rules | Outfit scoring & ranking |

## Scoring Breakdown

```
Total Score = 
  40% Color Harmony +
  30% Style Similarity +
  20% Occasion Fit +
  10% Item Variety
```

## Color Harmony Rules

| Type | Angle | Score |
|------|-------|-------|
| Complementary | 180° | 0.95 |
| Triadic | 120° | 0.90 |
| Analogous | ±30° | 0.85 |
| Split-Comp | ±150° | 0.80 |
| Neutral | Any | 0.80 |

## Performance

- **First Request**: ~3-5s (model loading)
- **Subsequent**: ~500ms-1s
- **Memory**: ~1-2GB
- **GPU**: Optional (TensorFlow auto-detects)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `taskkill /PID <pid> /F` |
| TensorFlow error | `pip install tensorflow>=2.16.0` |
| Slow predictions | Normal on first run (compilation) |
| Out of memory | Reduce `max_size` in `color_analyzer.py` |

## File Structure

```
backend/
├── main.py                 # FastAPI server
├── ml_classifier.py        # ResNet50 classifier
├── color_analyzer.py       # K-means + color theory
├── outfit_recommender.py   # Scoring engine
├── test_ml.py             # Test suite
├── requirements.txt       # Dependencies
└── README.md             # Full documentation
```

## Testing

```python
# Test classification
from ml_classifier import get_classifier
classifier = get_classifier()
prediction = classifier.predict(image_bytes)

# Test color extraction
from color_analyzer import get_color_analyzer
analyzer = get_color_analyzer()
colors = analyzer.extract_colors(image_bytes)

# Test recommendations
from outfit_recommender import get_outfit_recommender
recommender = get_outfit_recommender()
outfits = recommender.recommend_outfits(items, 'formal')
```

## Key Features

✅ Real ResNet50 (not mock!)  
✅ Multi-color extraction with K-means  
✅ Color theory harmony scoring  
✅ Deep learning style similarity  
✅ 6 occasion types with custom rules  
✅ Lazy model loading  
✅ Automatic image preprocessing  
✅ Error handling & fallbacks  

## Documentation

- **Full Docs**: `ML_SYSTEM_DOCUMENTATION.md`
- **API Docs**: http://localhost:8000/docs
- **Setup Guide**: `README.md`
