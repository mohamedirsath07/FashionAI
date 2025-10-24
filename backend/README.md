# Mock ML Backend for Fashion-Style

This is a simple FastAPI backend that provides mock AI-powered outfit recommendations.

## Features

- `/predict-type` - Mock clothing type detection (returns random types)
- `/recommend-outfits` - Mock outfit recommendations (generates 3 combinations)

## Setup

### 1. Install Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

**Note:** If you see a warning about scripts not being in PATH, that's normal. You can either:
- Add `C:\Users\<YourUser>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.X_xxxxx\LocalCache\local-packages\Python3X\Scripts` to your PATH
- Or ignore it (the scripts will still work)

### 2. Start the Backend

```powershell
# From the backend folder
python main.py
```

Or using uvicorn directly:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Verify It's Running

Open http://localhost:8000/docs in your browser. You should see the FastAPI interactive documentation.

## How It Works

### Mock Type Detection
- Returns a random clothing type (top, bottom, shoes, dress, blazer, other)
- Confidence scores between 60-98%

### Mock Recommendations
- Generates 3 outfit combinations
- Each outfit has 1 top + 1 bottom (if max_items >= 2)
- Random match scores between 50-95%
- Uses placeholder SVG images from `/uploads/`

## Testing

### Test Type Detection
```powershell
curl -X POST http://localhost:8000/predict-type -F "file=@/path/to/image.jpg"
```

### Test Recommendations
```powershell
curl -X POST http://localhost:8000/recommend-outfits -F "occasion=casual" -F "max_items=2"
```

## Frontend Integration

The frontend will automatically:
1. Try to connect to this backend on port 8000
2. If backend is unavailable, fall back to client-side mock data
3. Show recommendations either way

## Upgrading to Real ML

To replace this with a real ML backend:

1. Install ML libraries:
   ```powershell
   pip install torch torchvision transformers pillow scikit-learn
   ```

2. Replace the mock functions in `main.py` with real ML model calls:
   - Load ResNet50 for type detection
   - Load Fashion-CLIP for outfit recommendations
   - Add color extraction with PIL

3. The frontend API contract will remain the same!

## Troubleshooting

### Port 8000 already in use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F
```

### CORS errors
The backend is configured with `allow_origins=["*"]` so CORS should work. If you still see issues, check your browser console.

### Images not loading
The mock images are SVG placeholders in `client/public/uploads/`. They're served by Vite, not this backend.

---

**The backend is now ready! Start it and your frontend will get AI recommendations.** 🎉
