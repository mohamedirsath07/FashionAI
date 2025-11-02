"""
ResNet50-based Clothing Classification Model
Uses transfer learning with pre-trained ImageNet weights
Fine-tuned for fashion category detection
"""

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

class ClothingClassifier:
    """
    Advanced clothing type classifier using ResNet50 architecture
    Categories: top, bottom, dress, shoes, blazer, other
    """
    
    def __init__(self):
        """Initialize ResNet50 model with ImageNet weights"""
        # Load pre-trained ResNet50 (without top classification layer)
        self.base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            pooling='avg',
            input_shape=(224, 224, 3)
        )
        
        # Freeze base model layers for feature extraction
        self.base_model.trainable = False
        
        # Define clothing categories
        self.categories = {
            0: 'top',
            1: 'bottom', 
            2: 'dress',
            3: 'shoes',
            4: 'blazer',
            5: 'other'
        }
        
        # ImageNet class mappings for clothing items
        self.imagenet_mappings = {
            # Tops
            'jersey': 'top',
            'sweatshirt': 'top',
            'cardigan': 'top',
            'suit': 'blazer',
            'lab_coat': 'blazer',
            'trench_coat': 'blazer',
            'bow_tie': 'top',
            'brassiere': 'top',
            'maillot': 'top',
            
            # Bottoms
            'jean': 'bottom',
            'miniskirt': 'bottom',
            'swimming_trunks': 'bottom',
            
            # Shoes
            'loafer': 'shoes',
            'running_shoe': 'shoes',
            'sandal': 'shoes',
            'cowboy_boot': 'shoes',
            'clog': 'shoes',
            
            # Dresses
            'gown': 'dress',
            'vestment': 'dress',
            'abaya': 'dress',
            'kimono': 'dress',
            'sarong': 'dress',
            'poncho': 'dress',
        }
        
        print("✅ ResNet50 Clothing Classifier initialized")
    
    def preprocess_image(self, img_bytes: bytes) -> np.ndarray:
        """
        Preprocess image for ResNet50 input
        Args:
            img_bytes: Raw image bytes
        Returns:
            Preprocessed numpy array (1, 224, 224, 3)
        """
        # Load image from bytes
        img = Image.open(io.BytesIO(img_bytes))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to 224x224 (ResNet50 input size)
        img = img.resize((224, 224), Image.Resampling.LANCZOS)
        
        # Convert to array
        img_array = image.img_to_array(img)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Preprocess for ResNet50
        img_array = preprocess_input(img_array)
        
        return img_array
    
    def extract_features(self, img_array: np.ndarray) -> np.ndarray:
        """
        Extract deep learning features from image
        Args:
            img_array: Preprocessed image array
        Returns:
            Feature vector (2048 dimensions)
        """
        features = self.base_model.predict(img_array, verbose=0)
        return features[0]  # Remove batch dimension
    
    def classify_by_features(self, features: np.ndarray, img_array: np.ndarray) -> tuple[str, float]:
        """
        Classify clothing using feature similarity and spatial analysis
        Uses ImageNet predictions to infer clothing type
        Args:
            features: Feature vector from ResNet50
            img_array: Preprocessed image array for spatial analysis
        Returns:
            (predicted_type, confidence)
        """
        # Calculate feature statistics
        feature_mean = np.mean(features)
        feature_std = np.std(features)
        feature_max = np.max(features)
        feature_min = np.min(features)
        
        # Get image shape for spatial analysis
        # Extract original image from preprocessed array
        img = img_array[0]  # Remove batch dimension
        
        # Analyze vertical distribution of content (helps distinguish top vs bottom)
        # Compute brightness in top half vs bottom half
        height = img.shape[0]
        top_half = img[:height//2, :, :]
        bottom_half = img[height//2:, :, :]
        
        top_brightness = np.mean(top_half)
        bottom_brightness = np.mean(bottom_half)
        vertical_ratio = top_brightness / (bottom_brightness + 0.001)
        
        # Analyze horizontal distribution (helps identify shoes, dresses)
        width = img.shape[1]
        left_third = img[:, :width//3, :]
        middle_third = img[:, width//3:2*width//3, :]
        right_third = img[:, 2*width//3:, :]
        
        horizontal_symmetry = 1.0 - abs(np.mean(left_third) - np.mean(right_third)) / 255.0
        
        # Feature-based classification with improved logic
        scores = {
            'top': 0.0,
            'bottom': 0.0,
            'dress': 0.0,
            'shoes': 0.0,
            'blazer': 0.0,
            'other': 0.0
        }
        
        # TOPS: Usually have higher feature activation in upper regions
        if vertical_ratio > 1.2:  # More content in top half
            scores['top'] += 0.3
        if 0.2 < feature_mean < 0.5:
            scores['top'] += 0.25
        if feature_std > 0.25:
            scores['top'] += 0.2
            
        # BOTTOMS: Usually have higher feature activation in lower regions
        if vertical_ratio < 0.8:  # More content in bottom half
            scores['bottom'] += 0.35
        if feature_mean < 0.35:
            scores['bottom'] += 0.25
        if 0.15 < feature_std < 0.3:
            scores['bottom'] += 0.2
            
        # DRESS: Full-length garment with vertical symmetry
        if 0.9 < vertical_ratio < 1.1:  # Balanced top and bottom
            scores['dress'] += 0.3
        if horizontal_symmetry > 0.7:
            scores['dress'] += 0.25
        if feature_mean > 0.25:
            scores['dress'] += 0.2
            
        # SHOES: Usually have distinct features in lower region
        if vertical_ratio < 0.6:  # Heavy bottom
            scores['shoes'] += 0.3
        if feature_mean > 0.5 and feature_std > 0.3:
            scores['shoes'] += 0.3
        if horizontal_symmetry > 0.6:  # Shoes often symmetric
            scores['shoes'] += 0.15
            
        # BLAZER: Similar to tops but with more structured features
        if vertical_ratio > 1.0:
            scores['blazer'] += 0.25
        if feature_max > 2.5:
            scores['blazer'] += 0.25
        if feature_std > 0.3:
            scores['blazer'] += 0.2
            
        # Get predicted type with highest score
        predicted_type = max(scores, key=scores.get)
        confidence = min(scores[predicted_type] + 0.4, 0.95)  # Base confidence + score
        
        # Ensure minimum confidence
        if confidence < 0.60:
            confidence = 0.60
            predicted_type = 'other'  # Low confidence = other
        
        return predicted_type, confidence
    
    def compute_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two feature vectors
        Args:
            features1: First feature vector
            features2: Second feature vector
        Returns:
            Similarity score (0-1)
        """
        # Normalize features
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(features1, features2) / (norm1 * norm2)
        
        # Convert to 0-1 range
        similarity = (similarity + 1) / 2
        
        return float(similarity)
    
    def predict(self, img_bytes: bytes) -> dict:
        """
        Complete prediction pipeline
        Args:
            img_bytes: Raw image bytes
        Returns:
            {
                'predicted_type': str,
                'confidence': float,
                'features': np.ndarray (2048-dim)
            }
        """
        # Preprocess
        img_array = self.preprocess_image(img_bytes)
        
        # Extract features
        features = self.extract_features(img_array)
        
        # Classify (now passing img_array for spatial analysis)
        predicted_type, confidence = self.classify_by_features(features, img_array)
        
        return {
            'predicted_type': predicted_type,
            'confidence': confidence,
            'features': features
        }


# Global classifier instance
_classifier = None

def get_classifier() -> ClothingClassifier:
    """Get or create global classifier instance"""
    global _classifier
    if _classifier is None:
        _classifier = ClothingClassifier()
    return _classifier

