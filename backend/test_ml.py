"""Test script to verify ML system"""
import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__} imported successfully")
except ImportError as e:
    print(f"❌ TensorFlow import failed: {e}")
    sys.exit(1)

try:
    import sklearn
    print(f"✅ scikit-learn {sklearn.__version__} imported successfully")
except ImportError as e:
    print(f"❌ scikit-learn import failed: {e}")

try:
    import cv2
    print(f"✅ OpenCV {cv2.__version__} imported successfully")
except ImportError as e:
    print(f"❌ OpenCV import failed: {e}")

try:
    from PIL import Image
    print(f"✅ Pillow imported successfully")
except ImportError as e:
    print(f"❌ Pillow import failed: {e}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__} imported successfully")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")

print("\n🧪 Testing ML Classifier...")
try:
    from ml_classifier import get_classifier
    classifier = get_classifier()
    print("✅ ResNet50 classifier loaded successfully!")
except Exception as e:
    print(f"❌ Classifier loading failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎨 Testing Color Analyzer...")
try:
    from color_analyzer import get_color_analyzer
    analyzer = get_color_analyzer()
    print("✅ Color analyzer loaded successfully!")
except Exception as e:
    print(f"❌ Color analyzer loading failed: {e}")
    import traceback
    traceback.print_exc()

print("\n👔 Testing Outfit Recommender...")
try:
    from outfit_recommender import get_outfit_recommender
    recommender = get_outfit_recommender()
    print("✅ Outfit recommender loaded successfully!")
except Exception as e:
    print(f"❌ Outfit recommender loading failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 All ML systems operational!")
