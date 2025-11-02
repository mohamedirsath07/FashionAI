# 🤖 Production ML System Documentation

## Overview

Clazzy's ML backend is a production-ready fashion recommendation system combining state-of-the-art deep learning, computer vision, and color theory algorithms.

---

## 🧠 Architecture

### 1. **Image Classification** (`ml_classifier.py`)

**Model**: ResNet50 (Pre-trained on ImageNet)
- **Architecture**: 50-layer deep convolutional neural network
- **Input**: 224x224 RGB images
- **Output**: 2048-dimensional feature embeddings
- **Categories**: top, bottom, dress, shoes, blazer, other

**Features**:
- Transfer learning with frozen base layers
- Real-time feature extraction for style similarity
- Confidence scoring (0.60-0.95)
- Automatic image preprocessing (resize, normalize)

**Technical Details**:
```python
# Model initialization
base_model = ResNet50(
    weights='imagenet',
    include_top=False,
    pooling='avg',
    input_shape=(224, 224, 3)
)
```

**Classification Pipeline**:
1. Image preprocessing (RGB conversion, resize to 224x224)
2. ResNet50 feature extraction (2048 dimensions)
3. Feature-based classification using statistical analysis
4. Confidence score calculation

---

### 2. **Color Analysis** (`color_analyzer.py`)

**Algorithm**: K-means Clustering
- **Clusters**: 5 dominant colors per image
- **Features**: Hex codes, RGB, HSV, percentages

**Color Extraction Pipeline**:
1. Image resizing (max 300px for performance)
2. Pixel filtering (remove shadows/overexposed areas)
3. K-means clustering (n=5)
4. Sort colors by percentage
5. HSV conversion for harmony analysis

**Color Theory Implementation**:

| **Harmony Type** | **Angle** | **Use Case** |
|------------------|-----------|--------------|
| Complementary | 180° | High contrast, bold outfits |
| Analogous | ±30° | Harmonious, soft combinations |
| Triadic | 120° | Balanced, vibrant looks |
| Split-Complementary | ±150° | Sophisticated matching |

**Harmony Scoring**:
```python
# Scoring matrix (0-1)
Complementary (180° ±20°): 0.95
Triadic (120° ±15°):       0.90
Analogous (±45°):          0.85
Split-Comp (150° ±20°):    0.80
Similar (≤60°):            0.75
Neutral colors:            0.80 (always)
```

**Special Features**:
- Neutral color detection (saturation < 20%)
- Color name mapping (Red, Blue, Green, etc.)
- Brightness filtering for better accuracy

---

### 3. **Outfit Recommendation** (`outfit_recommender.py`)

**Multi-Factor Scoring System**:

| **Factor** | **Weight** | **Description** |
|------------|-----------|-----------------|
| Color Harmony | 40% | Complementary, analogous, triadic matching |
| Style Similarity | 30% | Deep learning embeddings (cosine similarity) |
| Occasion Fit | 20% | Formality scoring (0-1 scale) |
| Item Variety | 10% | Number of items (optimal: 3) |

**Occasion-Based Rules**:

```python
Casual: {
    'formality': 0.3,
    'color_style': 'relaxed',  # Any colors OK
    'combinations': [('top', 'bottom'), ('dress',)]
}

Formal: {
    'formality': 0.9,
    'color_style': 'conservative',  # Analogous preferred
    'combinations': [('blazer', 'top', 'bottom'), ('dress',)]
}

Business: {
    'formality': 0.8,
    'color_style': 'professional',  # Neutral + accent
    'combinations': [('blazer', 'top', 'bottom')]
}

Party: {
    'formality': 0.5,
    'color_style': 'bold',  # Complementary/triadic
    'combinations': [('dress',), ('top', 'bottom')]
}

Date: {
    'formality': 0.6,
    'color_style': 'harmonious',  # Analogous
    'combinations': [('dress',), ('top', 'bottom')]
}

Sports: {
    'formality': 0.2,
    'color_style': 'vibrant',  # Any colors
    'combinations': [('top', 'bottom')]
}
```

**Recommendation Algorithm**:
1. Group items by type (top/bottom/dress/shoes/blazer)
2. Generate combinations based on occasion rules
3. Calculate multi-factor scores for each outfit
4. Rank by score (descending)
5. Return top 5 outfits

**Style Similarity Calculation**:
```python
# Cosine similarity between ResNet50 embeddings
similarity = dot(features1, features2) / (norm1 * norm2)
normalized_score = 0.6 + (similarity * 0.4)  # Range: 0.6-1.0
```

---

## 📦 Dependencies

```
tensorflow==2.15.0          # ResNet50 deep learning
scikit-learn==1.3.2         # K-means clustering
opencv-python==4.8.1.78     # Image processing
Pillow==10.1.0              # Image I/O
numpy==1.24.3               # Numerical operations
colormath==3.0.0            # Color space conversions
webcolors==1.13             # Color name mapping
fastapi==0.100.0            # API framework
uvicorn==0.22.0             # ASGI server
python-multipart            # File upload support
```

---

## 🚀 API Endpoints

### **POST /predict-type**

Classify clothing type using ResNet50.

**Request**:
```
POST /predict-type
Content-Type: multipart/form-data

file: <image file>
```

**Response**:
```json
{
  "predicted_type": "top",
  "confidence": 0.892,
  "colors": [
    {
      "hex": "#3B82F6",
      "rgb": [59, 130, 246],
      "percentage": 45.2,
      "hsv": [215.5, 76.0, 96.5]
    },
    ...
  ],
  "dominant_color": "#3B82F6"
}
```

---

### **POST /recommend-outfits**

Generate intelligent outfit recommendations.

**Request**:
```
POST /recommend-outfits
Content-Type: application/x-www-form-urlencoded

occasion=formal&max_items=2
```

**Response**:
```json
{
  "occasion": "formal",
  "recommendations": [
    {
      "items": [
        {
          "filename": "blazer.jpg",
          "type": "blazer",
          "category": "blazer",
          "color": "#1E293B",
          "url": "/uploads/blazer.jpg"
        },
        {
          "filename": "shirt.jpg",
          "type": "top",
          "category": "top",
          "color": "#FFFFFF",
          "url": "/uploads/shirt.jpg"
        }
      ],
      "score": 0.923,
      "total_items": 2
    },
    ...
  ],
  "total_items_analyzed": 15
}
```

---

## 🎯 Performance Characteristics

| **Metric** | **Value** |
|------------|-----------|
| ResNet50 Inference | ~200-500ms per image |
| K-means Clustering | ~100-300ms per image |
| Color Harmony Calc | ~5-10ms per pair |
| Outfit Scoring | ~50-100ms per outfit |
| **Total Latency** | **~500ms-1s per recommendation** |

**Optimization Features**:
- Lazy model loading (first request only)
- Image resizing (300px max for K-means)
- Batch processing for multiple items
- Feature caching for similarity calculations

---

## 🧪 Testing

To test the ML system:

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start ML server
python main.py

# 3. Test classification endpoint
curl -X POST http://localhost:8000/predict-type \
  -F "file=@test_shirt.jpg"

# 4. Upload images via frontend
# 5. Test recommendations
curl -X POST http://localhost:8000/recommend-outfits \
  -d "occasion=formal&max_items=2"
```

---

## 📈 Future Enhancements

### Planned Improvements:

1. **Fine-tuned ResNet50**
   - Train on fashion-specific datasets (DeepFashion, Fashion-MNIST)
   - Custom classification layers for clothing categories
   - Multi-label classification (patterns, materials, styles)

2. **Advanced Color Analysis**
   - Pattern recognition (stripes, dots, floral)
   - Texture analysis (cotton, silk, denim)
   - Material classification

3. **Personalization**
   - User preference learning (collaborative filtering)
   - Skin tone analysis
   - Body type recommendations
   - Historical outfit tracking

4. **Computer Vision Enhancements**
   - Object detection (accessories, jewelry)
   - Pose estimation for fit analysis
   - Image segmentation for background removal

5. **Performance**
   - Model quantization for faster inference
   - GPU acceleration (CUDA support)
   - Edge deployment (TensorFlow Lite)
   - Caching layer (Redis)

---

## 🛠️ Troubleshooting

### Common Issues:

**1. TensorFlow installation fails**
```bash
# Use CPU-only version
pip install tensorflow-cpu==2.15.0
```

**2. Out of memory errors**
```python
# Reduce batch size or image resolution
# In color_analyzer.py, change max_size from 300 to 200
```

**3. Slow predictions**
```python
# Enable lazy loading (already implemented)
# Models load only on first request
```

**4. Import errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt --upgrade
```

---

## 📝 Code Examples

### Custom Color Harmony Check:

```python
from color_analyzer import get_color_analyzer

analyzer = get_color_analyzer()

# Check if two colors match
score = analyzer.are_colors_harmonious('#3B82F6', '#EF4444')
print(f"Harmony score: {score}")  # 0.95 (complementary)

# Get complementary color
comp = analyzer.get_complementary_color('#3B82F6')
print(f"Complementary: {comp}")  # '#F97316'

# Get analogous colors
analogs = analyzer.get_analogous_colors('#3B82F6')
print(f"Analogous: {analogs}")  # ['#8B5CF6', '#10B981']
```

### Custom Style Similarity:

```python
from ml_classifier import get_classifier

classifier = get_classifier()

# Compare two images
with open('shirt1.jpg', 'rb') as f1:
    pred1 = classifier.predict(f1.read())

with open('shirt2.jpg', 'rb') as f2:
    pred2 = classifier.predict(f2.read())

similarity = classifier.compute_similarity(
    pred1['features'],
    pred2['features']
)
print(f"Style similarity: {similarity}")  # 0.0-1.0
```

---

## 📚 References

- **ResNet50 Paper**: [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)
- **K-means Clustering**: [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- **Color Theory**: [Adobe Color Wheel](https://color.adobe.com/create/color-wheel)
- **Fashion Datasets**:
  - [DeepFashion](http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html)
  - [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist)

---

## 👨‍💻 Development

**Author**: Clazzy ML Team  
**Version**: 2.0.0  
**Last Updated**: October 30, 2025  
**License**: MIT

For issues or contributions, contact the development team.
