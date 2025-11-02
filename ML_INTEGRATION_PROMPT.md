# ML Model Integration Prompt - Add AI Recommendations to Existing App

## Context
I have a working fashion app with frontend and backend. I want to ADD AI-powered outfit recommendations using ML models (ResNet50 + Fashion-CLIP) and intelligent color combination suggestions. The backend already has these ML features implemented - I just need to integrate them into my existing frontend.

## What I Want to Add

### 1. ML-Powered Clothing Type Detection
### 2. AI Outfit Recommendations Based on Occasion
### 3. Intelligent Color Combination Suggestions

---

## Backend ML Endpoints Available

### Endpoint 1: AI Clothing Type Detection
**Purpose**: Automatically classify uploaded clothing images using ResNet50 ML model

```typescript
POST /predict-type
Content-Type: multipart/form-data

// Request
const formData = new FormData();
formData.append('file', imageFile);

fetch(`${API_BASE_URL}/predict-type`, {
  method: 'POST',
  body: formData
});

// Response
{
  "predicted_type": "top" | "bottom" | "shoes" | "dress" | "blazer" | "other",
  "confidence": 0.85
}
```

**When to Use**: 
- When user uploads an image and you can't determine type from filename
- To auto-classify user's wardrobe items
- To correct misclassified items

**Integration Example**:
```typescript
// In your image upload handler
const detectClothingType = async (file: File): Promise<string> => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await fetch(`${API_BASE_URL}/predict-type`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Type detection failed');
    
    const data = await response.json();
    return data.predicted_type; // 'top', 'bottom', 'shoes', etc.
    
  } catch (error) {
    console.error('ML prediction failed:', error);
    return 'other'; // Fallback
  }
};

// Use it when uploading
const handleUpload = async (files: File[]) => {
  const types = await Promise.all(
    files.map(file => detectClothingType(file))
  );
  
  // Now upload with ML-detected types
  // ... rest of upload logic
};
```

---

### Endpoint 2: AI Outfit Recommendations
**Purpose**: Get complete outfit combinations based on occasion using ML similarity matching

```typescript
POST /recommend-outfits
Content-Type: multipart/form-data

// Request
const formData = new FormData();
formData.append('occasion', 'casual'); // or 'formal', 'business', 'party', 'date', 'sports'
formData.append('max_items', '4');

fetch(`${API_BASE_URL}/recommend-outfits`, {
  method: 'POST',
  body: formData
});

// Response
{
  "occasion": "casual",
  "recommendations": [
    {
      "items": [
        {
          "filename": "uuid__top.jpg",
          "type": "top",
          "category": "top",
          "color": "#3B82F6",
          "url": "/uploads/uuid__top.jpg"
        },
        {
          "filename": "uuid__bottom.jpg",
          "type": "bottom",
          "category": "bottom",
          "color": "#1F2937",
          "url": "/uploads/uuid__bottom.jpg"
        },
        {
          "filename": "uuid__shoes.jpg",
          "type": "shoes",
          "category": "shoes",
          "color": "#FFFFFF",
          "url": "/uploads/uuid__shoes.jpg"
        }
      ],
      "score": 0.87,      // ML confidence score (0-1)
      "total_items": 3
    },
    // ... more outfit combinations
  ],
  "total_items_analyzed": 15
}
```

**Occasions Supported**:
- `casual` - Everyday comfortable wear
- `formal` - Business formal, weddings, ceremonies
- `business` - Professional office attire
- `party` - Festive, celebratory events
- `date` - Romantic outings
- `sports` - Athletic, gym wear

**Integration Example**:
```typescript
// Add to your existing component
const [recommendations, setRecommendations] = useState<OutfitRecommendation[]>([]);
const [selectedOccasion, setSelectedOccasion] = useState('casual');

const getAIRecommendations = async () => {
  setLoading(true);
  
  const formData = new FormData();
  formData.append('occasion', selectedOccasion);
  formData.append('max_items', '4');
  
  try {
    const response = await fetch(`${API_BASE_URL}/recommend-outfits`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) throw new Error('Recommendation failed');
    
    const result = await response.json();
    setRecommendations(result.recommendations);
    
  } catch (error) {
    console.error('AI recommendation failed:', error);
    setError('Failed to get recommendations');
  } finally {
    setLoading(false);
  }
};

// Add button in your UI
<button onClick={getAIRecommendations}>
  Get AI Outfit Recommendations
</button>

// Display recommendations
{recommendations.map((outfit, index) => (
  <div key={index} className="outfit-card">
    <h3>Outfit #{index + 1}</h3>
    <p>Match Score: {(outfit.score * 100).toFixed(0)}%</p>
    
    <div className="outfit-items">
      {outfit.items.map((item, i) => (
        <img 
          key={i}
          src={`${API_BASE_URL}${item.url}`}
          alt={item.type}
        />
      ))}
    </div>
  </div>
))}
```

---

### Endpoint 3: Color Combination Analysis
**Purpose**: Get intelligent color matching suggestions based on color theory

```typescript
// This endpoint analyzes your wardrobe colors and suggests combinations
// Backend has color theory rules built-in (complementary, analogous, triadic)

// Example: Get color suggestions for a specific item
const getColorMatches = (itemColor: string, wardrobeColors: string[]) => {
  // Backend automatically applies color theory when generating recommendations
  // Colors are analyzed during /recommend-outfits call
  
  // You can also implement frontend color matching:
  const complementary = getComplementaryColor(itemColor);
  const analogous = getAnalogousColors(itemColor);
  
  return { complementary, analogous };
};
```

**Color Theory Rules (Built into Backend)**:
- **Complementary**: Opposite colors on color wheel (high contrast)
- **Analogous**: Adjacent colors (harmonious)
- **Triadic**: Three evenly spaced colors (balanced)
- **Monochromatic**: Different shades of same color

---

## Integration Steps

### Step 1: Add ML Type Detection to Upload Flow

In your existing upload component:

```typescript
// BEFORE (without ML)
const handleUpload = async (files: File[]) => {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
    formData.append('types', 'unknown'); // Generic type
  });
  
  await uploadToBackend(formData);
};

// AFTER (with ML)
const handleUpload = async (files: File[]) => {
  const formData = new FormData();
  
  // Use ML to detect types
  const types = await Promise.all(
    files.map(async (file) => {
      // Quick filename check first
      if (file.name.toLowerCase().includes('shirt')) return 'top';
      if (file.name.toLowerCase().includes('pant')) return 'bottom';
      
      // Use ML for unknown
      return await detectClothingType(file);
    })
  );
  
  files.forEach((file, i) => {
    formData.append('files', file);
    formData.append('types', types[i]);
  });
  
  await uploadToBackend(formData);
};
```

### Step 2: Add AI Recommendation Button

In your wardrobe/outfit page:

```typescript
// Add to your component state
const [occasion, setOccasion] = useState('casual');
const [aiRecommendations, setAiRecommendations] = useState([]);

// Add occasion selector
<select value={occasion} onChange={(e) => setOccasion(e.target.value)}>
  <option value="casual">Casual</option>
  <option value="formal">Formal</option>
  <option value="business">Business</option>
  <option value="party">Party</option>
  <option value="date">Date</option>
  <option value="sports">Sports</option>
</select>

// Add recommendation button
<button onClick={getAIRecommendations} disabled={loading}>
  {loading ? 'Analyzing...' : 'Get AI Recommendations'}
</button>

// Display results
{aiRecommendations.length > 0 && (
  <div className="recommendations">
    <h2>AI-Powered Outfit Suggestions for {occasion}</h2>
    {aiRecommendations.map((outfit, index) => (
      <OutfitCard key={index} outfit={outfit} />
    ))}
  </div>
)}
```

### Step 3: Display Color-Coded Items

Add visual color indicators:

```typescript
// Color badge component
const ColorBadge = ({ color, type }: { color: string, type: string }) => (
  <div className="flex items-center gap-2">
    <div 
      className="w-4 h-4 rounded-full border"
      style={{ backgroundColor: color }}
    />
    <span className="text-sm">{type}</span>
  </div>
);

// Use in wardrobe display
{wardrobeItems.map(item => (
  <div key={item.id}>
    <img src={item.url} alt={item.type} />
    <ColorBadge color={item.color} type={item.type} />
  </div>
))}
```

### Step 4: Add Match Score Visualization

Show how well items match:

```typescript
const ScoreBadge = ({ score }: { score: number }) => {
  const percentage = Math.round(score * 100);
  const color = percentage > 80 ? 'green' : percentage > 60 ? 'yellow' : 'gray';
  
  return (
    <div className={`badge ${color}`}>
      Match: {percentage}%
    </div>
  );
};

// Use in recommendations
<ScoreBadge score={outfit.score} />
```

---

## TypeScript Interfaces

```typescript
interface ClothingItem {
  filename: string;
  type: 'top' | 'bottom' | 'shoes' | 'dress' | 'blazer' | 'other';
  category?: string;
  color: string; // Hex color
  url: string;
}

interface OutfitRecommendation {
  items: ClothingItem[];
  score: number; // 0-1 confidence score
  occasion: string;
  total_items: number;
}

interface RecommendationResponse {
  occasion: string;
  recommendations: OutfitRecommendation[];
  total_items_analyzed: number;
}
```

---

## UI/UX Suggestions

### 1. Loading States
```typescript
{loading && (
  <div className="loading">
    <Spinner />
    <p>AI is analyzing your wardrobe...</p>
  </div>
)}
```

### 2. Match Score Indicators
```typescript
const getScoreColor = (score: number) => {
  if (score > 0.8) return 'text-green-600';
  if (score > 0.6) return 'text-yellow-600';
  return 'text-gray-600';
};

<span className={getScoreColor(outfit.score)}>
  {(outfit.score * 100).toFixed(0)}% Match
</span>
```

### 3. Occasion Icons
```typescript
const occasionIcons = {
  casual: '👕',
  formal: '🎩',
  business: '💼',
  party: '🎉',
  date: '💕',
  sports: '⚽'
};

<span>{occasionIcons[occasion]} {occasion}</span>
```

### 4. Empty State
```typescript
{aiRecommendations.length === 0 && (
  <div className="empty-state">
    <p>Upload at least 3 clothing items to get AI recommendations</p>
    <button onClick={openUploader}>Upload Clothes</button>
  </div>
)}
```

---

## Backend Setup (Quick Reference)

Your backend should already have these, but verify:

### 1. ML Model Files
```
backend/
  ├── main.py (FastAPI endpoints)
  ├── outfit_recommender.py (ML logic - ResNet50 + Fashion-CLIP)
  └── requirements.txt (torch, torchvision, transformers)
```

### 2. Start Backend
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Required Python Packages
```
fastapi==0.115.0
torch==2.5.1
torchvision==0.20.1
transformers==4.57.1
Pillow==10.0.1
scikit-learn==1.3.2
```

---

## Testing Checklist

- [ ] ML type detection works for uploaded images
- [ ] AI recommendations return 3-5 outfit combinations
- [ ] Match scores are displayed correctly (0-100%)
- [ ] Color badges show item colors
- [ ] Occasion selector changes recommendations
- [ ] Loading states display during API calls
- [ ] Error handling for failed ML predictions
- [ ] Images load from backend (/uploads/ endpoint)
- [ ] Recommendations include top + bottom + shoes when available
- [ ] Empty state shows when no items uploaded

---

## Common Issues & Solutions

### Issue 1: "No recommendations returned"
**Cause**: Not enough wardrobe items
**Solution**: Need minimum 3 items (at least 1 top, 1 bottom)

### Issue 2: "ML prediction returns 'other'"
**Cause**: Image quality too low or unusual clothing
**Solution**: Add fallback type selector for users to manually correct

### Issue 3: "CORS error on /predict-type"
**Cause**: Backend CORS not configured
**Solution**: Backend should have `allow_origins=["*"]` or your frontend URL

### Issue 4: "Low match scores (<50%)"
**Cause**: Limited wardrobe variety or mismatched colors
**Solution**: This is expected - show all recommendations regardless

---

## Task

Please integrate the ML-powered recommendation features into my existing frontend by:

1. **Adding ML type detection** to the image upload flow using `/predict-type` endpoint
2. **Adding an AI recommendation button** that calls `/recommend-outfits` with selected occasion
3. **Displaying recommendations** with match scores, color badges, and outfit images
4. **Adding occasion selector** (casual, formal, business, party, date, sports)
5. **Showing visual indicators** for match quality (color-coded scores)

Keep my existing UI/UX style and components - just add these new AI features on top. Make sure to use the dynamic `API_BASE_URL` pattern for network compatibility:

```typescript
const API_BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
```
