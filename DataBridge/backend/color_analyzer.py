"""
Advanced Color Analysis System
Uses K-means clustering for multi-color extraction
Implements comprehensive color theory for outfit color matching
Features: Better extraction, color naming, advanced color schemes
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import io
from typing import List, Tuple, Dict
import colorsys

class ColorAnalyzer:
    """
    Advanced color extraction and harmony analysis with color naming
    """
    
    def __init__(self):
        """Initialize color analyzer with color database"""
        self.n_colors = 5  # Extract top 5 colors
        
        # Comprehensive color name database
        self.color_names = {
            # Reds
            (255, 0, 0): 'Red', (220, 20, 60): 'Crimson', (178, 34, 34): 'Firebrick',
            (255, 69, 0): 'Red Orange', (255, 99, 71): 'Tomato', (250, 128, 114): 'Salmon',
            
            # Pinks
            (255, 192, 203): 'Pink', (255, 182, 193): 'Light Pink', (219, 112, 147): 'Pale Violet Red',
            (255, 20, 147): 'Deep Pink', (199, 21, 133): 'Medium Violet Red', (255, 0, 255): 'Magenta',
            (255, 105, 180): 'Hot Pink',
            
            # Oranges
            (255, 165, 0): 'Orange', (255, 140, 0): 'Dark Orange', (255, 127, 80): 'Coral',
            (255, 160, 122): 'Light Salmon', (255, 218, 185): 'Peach',
            
            # Yellows
            (255, 255, 0): 'Yellow', (255, 215, 0): 'Gold', (255, 255, 224): 'Light Yellow',
            (255, 250, 205): 'Lemon', (240, 230, 140): 'Khaki',
            
            # Greens
            (0, 255, 0): 'Lime', (0, 128, 0): 'Green', (34, 139, 34): 'Forest Green',
            (144, 238, 144): 'Light Green', (143, 188, 143): 'Dark Sea Green',
            (107, 142, 35): 'Olive', (154, 205, 50): 'Yellow Green',
            
            # Blues
            (0, 0, 255): 'Blue', (0, 0, 139): 'Dark Blue', (0, 191, 255): 'Deep Sky Blue',
            (135, 206, 235): 'Sky Blue', (173, 216, 230): 'Light Blue',
            (70, 130, 180): 'Steel Blue', (100, 149, 237): 'Cornflower Blue',
            (0, 128, 128): 'Teal', (64, 224, 208): 'Turquoise', (0, 255, 255): 'Cyan',
            
            # Purples
            (128, 0, 128): 'Purple', (138, 43, 226): 'Blue Violet', (148, 0, 211): 'Dark Violet',
            (186, 85, 211): 'Medium Orchid', (221, 160, 221): 'Plum', (238, 130, 238): 'Violet',
            (75, 0, 130): 'Indigo', (147, 112, 219): 'Medium Purple',
            
            # Browns
            (165, 42, 42): 'Brown', (139, 69, 19): 'Saddle Brown', (160, 82, 45): 'Sienna',
            (210, 105, 30): 'Chocolate', (205, 133, 63): 'Peru', (244, 164, 96): 'Sandy Brown',
            (222, 184, 135): 'Burlywood', (210, 180, 140): 'Tan',
            
            # Neutrals
            (0, 0, 0): 'Black', (255, 255, 255): 'White', (128, 128, 128): 'Gray',
            (192, 192, 192): 'Silver', (211, 211, 211): 'Light Gray', (169, 169, 169): 'Dark Gray',
            (245, 245, 220): 'Beige', (255, 248, 220): 'Cornsilk', (250, 240, 230): 'Linen',
            (245, 222, 179): 'Wheat', (255, 228, 196): 'Bisque', (255, 235, 205): 'Blanched Almond',
            
            # Navy and Maroon
            (0, 0, 128): 'Navy', (25, 25, 112): 'Midnight Blue', (128, 0, 0): 'Maroon',
            (139, 0, 0): 'Dark Red', (85, 107, 47): 'Dark Olive Green',
        }
        
        print("✅ Color Analyzer initialized with K-means clustering and color naming")
    
    
    def extract_colors(self, img_bytes: bytes) -> List[dict]:
        """
        Extract dominant colors using K-means clustering with improved accuracy
        Args:
            img_bytes: Raw image bytes
        Returns:
            List of colors with hex codes, names, and percentages
            [
                {
                    'hex': '#FF5733',
                    'rgb': (255, 87, 51),
                    'name': 'Red Orange',
                    'percentage': 45.2,
                    'hsv': (9, 80, 100)
                },
                ...
            ]
        """
        # Load image
        img = Image.open(io.BytesIO(img_bytes))
        
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize for performance (max 400px for better accuracy)
        max_size = 400
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Reshape to 2D array of pixels (N, 3)
        pixels = img_array.reshape(-1, 3)
        
        # Advanced pixel filtering for better color extraction
        brightness = np.mean(pixels, axis=1)
        
        # Remove extreme values (shadows and highlights)
        mask = (brightness > 15) & (brightness < 240)
        filtered_pixels = pixels[mask]
        
        # Also filter out near-black and near-white pixels
        rgb_std = np.std(pixels, axis=1)
        color_mask = rgb_std > 10  # Pixels with some color variation
        filtered_pixels_2 = pixels[color_mask & mask]
        
        # Use filtered pixels if enough remain, otherwise use less strict filter
        if len(filtered_pixels_2) > 500:
            final_pixels = filtered_pixels_2
        elif len(filtered_pixels) > 200:
            final_pixels = filtered_pixels
        else:
            final_pixels = pixels
        
        # Apply K-means clustering with more iterations for accuracy
        n_clusters = min(self.n_colors, len(final_pixels))
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=15,  # More initializations
            max_iter=500  # More iterations
        )
        kmeans.fit(final_pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        # Get cluster labels
        labels = kmeans.labels_
        
        # Calculate color percentages
        label_counts = np.bincount(labels)
        percentages = (label_counts / len(labels)) * 100
        
        # Sort by percentage (descending)
        sorted_indices = np.argsort(percentages)[::-1]
        
        # Build result with color names
        result = []
        for idx in sorted_indices:
            color_rgb = tuple(colors[idx])
            color_hex = '#{:02x}{:02x}{:02x}'.format(*color_rgb)
            color_name = self.get_color_name(color_rgb)
            
            result.append({
                'hex': color_hex,
                'rgb': color_rgb,
                'name': color_name,
                'percentage': float(percentages[idx]),
                'hsv': self.rgb_to_hsv(color_rgb)
            })
        
        return result
    
    def get_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """
        Get human-readable color name from RGB
        Args:
            rgb: (R, G, B) tuple
        Returns:
            Color name string
        """
        # Check for neutrals first (low saturation)
        h, s, v = self.rgb_to_hsv(rgb)
        
        if s < 15:  # Very low saturation = neutral
            if v < 20:
                return 'Black'
            elif v > 90:
                return 'White'
            elif v > 70:
                return 'Light Gray'
            elif v < 40:
                return 'Dark Gray'
            else:
                return 'Gray'
        
        # Find closest color name from database
        min_distance = float('inf')
        closest_name = 'Unknown'
        
        for known_rgb, name in self.color_names.items():
            # Euclidean distance in RGB space
            distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(rgb, known_rgb)))
            
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        
        # If distance is too large, use hue-based naming
        if min_distance > 100:
            closest_name = self.get_hue_based_name(h, s, v)
        
        return closest_name
    
    def get_hue_based_name(self, h: float, s: float, v: float) -> str:
        """
        Get color name based on hue angle
        Args:
            h: Hue (0-360)
            s: Saturation (0-100)
            v: Value (0-100)
        Returns:
            Color name
        """
        # Add lightness/darkness prefix
        prefix = ''
        if v < 30:
            prefix = 'Dark '
        elif v > 80 and s < 50:
            prefix = 'Light '
        
        # Determine base color from hue
        if h < 15 or h >= 345:
            base = 'Red'
        elif h < 45:
            base = 'Orange'
        elif h < 75:
            base = 'Yellow'
        elif h < 150:
            base = 'Green'
        elif h < 210:
            base = 'Cyan'
        elif h < 270:
            base = 'Blue'
        elif h < 330:
            base = 'Purple'
        else:
            base = 'Pink'
        
        return prefix + base
    
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
    
    def get_split_complementary_colors(self, hex_color: str) -> List[str]:
        """
        Get split-complementary colors (base color + 2 adjacent to complement)
        Args:
            hex_color: Hex color code
        Returns:
            List of 2 split-complementary hex colors
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, v = self.rgb_to_hsv(rgb)
        
        # 150° and 210° (complement ± 30°)
        split1_h = (h + 150) % 360
        split2_h = (h + 210) % 360
        
        split1_rgb = self.hsv_to_rgb((split1_h, s, v))
        split2_rgb = self.hsv_to_rgb((split2_h, s, v))
        
        return [
            self.rgb_to_hex(split1_rgb),
            self.rgb_to_hex(split2_rgb)
        ]
    
    def get_tetradic_colors(self, hex_color: str) -> List[str]:
        """
        Get tetradic/double-complementary colors (rectangle on color wheel)
        Args:
            hex_color: Hex color code
        Returns:
            List of 3 tetradic hex colors
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, v = self.rgb_to_hsv(rgb)
        
        # 90°, 180°, 270° rotations
        tet1_h = (h + 90) % 360
        tet2_h = (h + 180) % 360
        tet3_h = (h + 270) % 360
        
        tet1_rgb = self.hsv_to_rgb((tet1_h, s, v))
        tet2_rgb = self.hsv_to_rgb((tet2_h, s, v))
        tet3_rgb = self.hsv_to_rgb((tet3_h, s, v))
        
        return [
            self.rgb_to_hex(tet1_rgb),
            self.rgb_to_hex(tet2_rgb),
            self.rgb_to_hex(tet3_rgb)
        ]
    
    def get_monochromatic_colors(self, hex_color: str) -> List[str]:
        """
        Get monochromatic colors (same hue, different saturation/value)
        Args:
            hex_color: Hex color code
        Returns:
            List of 4 monochromatic variations
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, v = self.rgb_to_hsv(rgb)
        
        variations = []
        
        # Lighter version (higher value, lower saturation)
        light_rgb = self.hsv_to_rgb((h, max(s - 30, 20), min(v + 20, 100)))
        variations.append(self.rgb_to_hex(light_rgb))
        
        # Darker version (lower value)
        dark_rgb = self.hsv_to_rgb((h, min(s + 10, 100), max(v - 30, 20)))
        variations.append(self.rgb_to_hex(dark_rgb))
        
        # More saturated
        saturated_rgb = self.hsv_to_rgb((h, min(s + 30, 100), v))
        variations.append(self.rgb_to_hex(saturated_rgb))
        
        # Less saturated (pastel)
        pastel_rgb = self.hsv_to_rgb((h, max(s - 40, 10), min(v + 10, 95)))
        variations.append(self.rgb_to_hex(pastel_rgb))
        
        return variations
    
    def get_all_color_schemes(self, hex_color: str) -> Dict[str, List[str]]:
        """
        Get all color schemes for a given color
        Args:
            hex_color: Base hex color
        Returns:
            Dictionary of all color schemes
        """
        return {
            'complementary': [self.get_complementary_color(hex_color)],
            'analogous': self.get_analogous_colors(hex_color),
            'triadic': self.get_triadic_colors(hex_color),
            'split_complementary': self.get_split_complementary_colors(hex_color),
            'tetradic': self.get_tetradic_colors(hex_color),
            'monochromatic': self.get_monochromatic_colors(hex_color)
        }
    
    def are_colors_harmonious(self, hex_color1: str, hex_color2: str) -> float:
        """
        Calculate comprehensive color harmony score (0-1)
        Based on multiple color theory relationships
        Args:
            hex_color1, hex_color2: Hex color codes
        Returns:
            Harmony score (0-1, higher is better)
        """
        rgb1 = self.hex_to_rgb(hex_color1)
        rgb2 = self.hex_to_rgb(hex_color2)
        
        h1, s1, v1 = self.rgb_to_hsv(rgb1)
        h2, s2, v2 = self.rgb_to_hsv(rgb2)
        
        # Calculate hue difference (0-180)
        hue_diff = abs(h1 - h2)
        if hue_diff > 180:
            hue_diff = 360 - hue_diff
        
        # Check for neutral colors (low saturation)
        is_neutral1 = s1 < 20
        is_neutral2 = s2 < 20
        
        # Neutrals work with everything
        if is_neutral1 or is_neutral2:
            return 0.85  # Good neutral match
        
        # Check for monochromatic (same hue)
        if hue_diff < 15:
            # Same color family - check value contrast
            value_diff = abs(v1 - v2)
            if value_diff > 30:
                return 0.88  # Good monochromatic contrast
            else:
                return 0.75  # Same colors, low contrast
        
        # Check for color harmony patterns
        score = 0.0
        
        # Complementary (180° ± 20°)
        if 160 <= hue_diff <= 200:
            score = 0.95  # Excellent - high contrast
        
        # Triadic (120° ± 15°)
        elif 105 <= hue_diff <= 135 or 225 <= hue_diff <= 255:
            score = 0.92  # Excellent - balanced
        
        # Tetradic/Square (90° ± 15°)
        elif 75 <= hue_diff <= 105 or 255 <= hue_diff <= 285:
            score = 0.90  # Very good - vibrant
        
        # Analogous (30° ± 15°)
        elif 15 <= hue_diff <= 45:
            score = 0.87  # Very good - harmonious
        
        # Split-complementary (150° ± 20°)
        elif 130 <= hue_diff <= 170 or 190 <= hue_diff <= 210:
            score = 0.82  # Good - sophisticated
        
        # Similar colors (45-75°)
        elif 45 < hue_diff <= 75:
            score = 0.78  # Good - related
        
        # Moderate difference (75-105°)
        elif 75 < hue_diff < 105:
            score = 0.70  # Acceptable
        
        # Poor harmony
        else:
            score = 0.55  # Below average
        
        # Bonus for complementary saturation/value
        sat_diff = abs(s1 - s2)
        val_diff = abs(v1 - v2)
        
        # Reward good contrast in value
        if val_diff > 25:
            score = min(score + 0.05, 1.0)
        
        # Slight penalty for extreme saturation mismatch
        if sat_diff > 60:
            score = max(score - 0.05, 0.5)
        
        return score
    
    def get_color_scheme_type(self, hex_color1: str, hex_color2: str) -> str:
        """
        Identify the color scheme type between two colors
        Args:
            hex_color1, hex_color2: Hex color codes
        Returns:
            Scheme name (complementary, analogous, triadic, etc.)
        """
        rgb1 = self.hex_to_rgb(hex_color1)
        rgb2 = self.hex_to_rgb(hex_color2)
        
        h1, s1, v1 = self.rgb_to_hsv(rgb1)
        h2, s2, v2 = self.rgb_to_hsv(rgb2)
        
        # Check for neutrals
        if s1 < 20 or s2 < 20:
            return 'neutral'
        
        # Calculate hue difference
        hue_diff = abs(h1 - h2)
        if hue_diff > 180:
            hue_diff = 360 - hue_diff
        
        # Identify scheme
        if hue_diff < 15:
            return 'monochromatic'
        elif 15 <= hue_diff <= 45:
            return 'analogous'
        elif 75 <= hue_diff <= 105:
            return 'tetradic'
        elif 105 <= hue_diff <= 135:
            return 'triadic'
        elif 130 <= hue_diff <= 170:
            return 'split-complementary'
        elif 160 <= hue_diff <= 200:
            return 'complementary'
        else:
            return 'custom'
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
