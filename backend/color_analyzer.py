"""
Advanced Color Analysis System
Uses K-means clustering for multi-color extraction
Implements color theory for complementary color matching
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import io
from typing import List, Tuple
import colorsys

class ColorAnalyzer:
    """
    Advanced color extraction and harmony analysis
    """
    
    def __init__(self):
        """Initialize color analyzer"""
        self.n_colors = 5  # Extract top 5 colors
        print("✅ Color Analyzer initialized with K-means clustering")
    
    def extract_colors(self, img_bytes: bytes) -> List[dict]:
        """
        Extract dominant colors using K-means clustering
        Args:
            img_bytes: Raw image bytes
        Returns:
            List of colors with hex codes and percentages
            [
                {'hex': '#FF5733', 'rgb': (255, 87, 51), 'percentage': 45.2},
                ...
            ]
        """
        # Load image
        img = Image.open(io.BytesIO(img_bytes))
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize for performance (max 300px)
        max_size = 300
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Reshape to 2D array of pixels (N, 3)
        pixels = img_array.reshape(-1, 3)
        
        # Remove very dark pixels (likely shadows/background)
        # Remove very light pixels (likely overexposed/background)
        brightness = np.mean(pixels, axis=1)
        mask = (brightness > 20) & (brightness < 235)
        filtered_pixels = pixels[mask]
        
        if len(filtered_pixels) < 100:
            # If too few pixels, use all
            filtered_pixels = pixels
        
        # Apply K-means clustering
        n_clusters = min(self.n_colors, len(filtered_pixels))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(filtered_pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        # Get cluster labels
        labels = kmeans.labels_
        
        # Calculate color percentages
        label_counts = np.bincount(labels)
        percentages = (label_counts / len(labels)) * 100
        
        # Sort by percentage (descending)
        sorted_indices = np.argsort(percentages)[::-1]
        
        # Build result
        result = []
        for idx in sorted_indices:
            color_rgb = tuple(colors[idx])
            color_hex = '#{:02x}{:02x}{:02x}'.format(*color_rgb)
            
            result.append({
                'hex': color_hex,
                'rgb': color_rgb,
                'percentage': float(percentages[idx]),
                'hsv': self.rgb_to_hsv(color_rgb)
            })
        
        return result
    
    def get_dominant_color(self, img_bytes: bytes) -> str:
        """
        Get single most dominant color
        Args:
            img_bytes: Raw image bytes
        Returns:
            Hex color code
        """
        colors = self.extract_colors(img_bytes)
        if colors:
            return colors[0]['hex']
        return '#808080'  # Gray fallback
    
    def rgb_to_hsv(self, rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """
        Convert RGB to HSV color space
        Args:
            rgb: (R, G, B) tuple (0-255)
        Returns:
            (H, S, V) tuple (H: 0-360, S: 0-100, V: 0-100)
        """
        r, g, b = [x / 255.0 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h * 360, s * 100, v * 100)
    
    def hsv_to_rgb(self, hsv: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """
        Convert HSV to RGB color space
        Args:
            hsv: (H, S, V) tuple (H: 0-360, S: 0-100, V: 0-100)
        Returns:
            (R, G, B) tuple (0-255)
        """
        h, s, v = hsv
        r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def get_complementary_color(self, hex_color: str) -> str:
        """
        Get complementary color (opposite on color wheel)
        Args:
            hex_color: Hex color code
        Returns:
            Complementary hex color
        """
        # Parse hex
        rgb = self.hex_to_rgb(hex_color)
        h, s, v = self.rgb_to_hsv(rgb)
        
        # Rotate hue by 180 degrees
        comp_h = (h + 180) % 360
        
        # Convert back
        comp_rgb = self.hsv_to_rgb((comp_h, s, v))
        return self.rgb_to_hex(comp_rgb)
    
    def get_analogous_colors(self, hex_color: str) -> List[str]:
        """
        Get analogous colors (adjacent on color wheel, ±30°)
        Args:
            hex_color: Hex color code
        Returns:
            List of 2 analogous hex colors
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, v = self.rgb_to_hsv(rgb)
        
        # ±30 degrees
        analog1_h = (h + 30) % 360
        analog2_h = (h - 30) % 360
        
        analog1_rgb = self.hsv_to_rgb((analog1_h, s, v))
        analog2_rgb = self.hsv_to_rgb((analog2_h, s, v))
        
        return [
            self.rgb_to_hex(analog1_rgb),
            self.rgb_to_hex(analog2_rgb)
        ]
    
    def get_triadic_colors(self, hex_color: str) -> List[str]:
        """
        Get triadic colors (120° apart on color wheel)
        Args:
            hex_color: Hex color code
        Returns:
            List of 2 triadic hex colors
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, v = self.rgb_to_hsv(rgb)
        
        # 120° and 240° rotations
        triad1_h = (h + 120) % 360
        triad2_h = (h + 240) % 360
        
        triad1_rgb = self.hsv_to_rgb((triad1_h, s, v))
        triad2_rgb = self.hsv_to_rgb((triad2_h, s, v))
        
        return [
            self.rgb_to_hex(triad1_rgb),
            self.rgb_to_hex(triad2_rgb)
        ]
    
    def are_colors_harmonious(self, hex_color1: str, hex_color2: str) -> float:
        """
        Calculate color harmony score (0-1)
        Based on complementary, analogous, and triadic relationships
        Args:
            hex_color1, hex_color2: Hex color codes
        Returns:
            Harmony score (0-1, higher is better)
        """
        rgb1 = self.hex_to_rgb(hex_color1)
        rgb2 = self.hex_to_rgb(hex_color2)
        
        h1, s1, v1 = self.rgb_to_hsv(rgb1)
        h2, s2, v2 = self.rgb_to_hsv(rgb2)
        
        # Calculate hue difference
        hue_diff = abs(h1 - h2)
        if hue_diff > 180:
            hue_diff = 360 - hue_diff
        
        # Check for color harmony patterns
        score = 0.0
        
        # Complementary (180° ± 20°)
        if 160 <= hue_diff <= 200:
            score = 0.95
        
        # Triadic (120° ± 15°)
        elif 105 <= hue_diff <= 135 or 225 <= hue_diff <= 255:
            score = 0.90
        
        # Analogous (30° ± 15°)
        elif hue_diff <= 45:
            score = 0.85
        
        # Split-complementary (150° ± 20°)
        elif 130 <= hue_diff <= 170:
            score = 0.80
        
        # Similar colors
        elif hue_diff <= 60:
            score = 0.75
        
        # Moderate difference
        elif 60 <= hue_diff <= 90:
            score = 0.65
        
        # Poor harmony
        else:
            score = 0.50
        
        # Adjust for saturation and value similarity
        sat_diff = abs(s1 - s2)
        val_diff = abs(v1 - v2)
        
        # Penalize extreme saturation/value differences
        if sat_diff > 50 or val_diff > 50:
            score *= 0.85
        
        # Bonus for neutral colors (works with everything)
        if s1 < 20 or s2 < 20:  # Low saturation = neutral
            score = max(score, 0.80)
        
        return score
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def get_color_name(self, hex_color: str) -> str:
        """
        Get human-readable color name
        Args:
            hex_color: Hex color code
        Returns:
            Color name (e.g., "Red", "Blue", "Neutral")
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, v = self.rgb_to_hsv(rgb)
        
        # Check for neutral colors
        if s < 20:
            if v > 80:
                return "White"
            elif v < 20:
                return "Black"
            else:
                return "Gray"
        
        # Determine hue-based color name
        if h < 15 or h >= 345:
            return "Red"
        elif h < 45:
            return "Orange"
        elif h < 75:
            return "Yellow"
        elif h < 165:
            return "Green"
        elif h < 255:
            return "Blue"
        elif h < 285:
            return "Purple"
        elif h < 345:
            return "Pink"
        else:
            return "Red"


# Global analyzer instance
_analyzer = None

def get_color_analyzer() -> ColorAnalyzer:
    """Get or create global color analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = ColorAnalyzer()
    return _analyzer
