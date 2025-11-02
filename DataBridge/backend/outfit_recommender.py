"""
Intelligent Outfit Recommendation Engine
Combines color theory, style similarity, and occasion-based matching
"""

import numpy as np
from typing import List, Dict, Tuple
from color_analyzer import get_color_analyzer
from ml_classifier import get_classifier

class OutfitRecommender:
    """
    Advanced outfit recommendation using:
    - Deep learning embeddings for style similarity
    - Color theory for harmony matching
    - Rule-based systems for occasion appropriateness
    """
    
    def __init__(self):
        """Initialize recommender with ML models"""
        self.color_analyzer = get_color_analyzer()
        self.classifier = get_classifier()
        
        # Occasion-based rules
        # IMPORTANT: Patterns must have complementary pieces (top+bottom, dress, etc.)
        # NEVER use patterns like (top, top) or (bottom, bottom)
        self.occasion_rules = {
            'casual': {
                'preferred_combinations': [
                    ('top', 'bottom'),           # Shirt + Pants (most common)
                    ('dress',),                   # Single dress
                    ('top', 'bottom', 'shoes'),  # Complete casual outfit
                ],
                'color_style': 'relaxed',  # Allow more variety
                'formality': 0.3
            },
            'formal': {
                'preferred_combinations': [
                    ('blazer', 'top', 'bottom'),  # Suit outfit
                    ('dress',),                    # Formal dress
                    ('top', 'bottom'),            # Dressy shirt + pants
                    ('blazer', 'dress'),          # Blazer over dress
                ],
                'color_style': 'conservative',  # Complementary or analogous
                'formality': 0.9
            },
            'business': {
                'preferred_combinations': [
                    ('blazer', 'top', 'bottom'),  # Professional suit
                    ('top', 'bottom'),            # Business casual
                    ('blazer', 'dress'),          # Professional dress
                    ('dress',),                   # Business dress
                ],
                'color_style': 'professional',  # Neutral + accent
                'formality': 0.8
            },
            'party': {
                'preferred_combinations': [
                    ('dress',),                   # Party dress
                    ('top', 'bottom'),            # Stylish top + pants
                    ('blazer', 'top', 'bottom'),  # Dressed up look
                    ('top', 'bottom', 'shoes'),  # Complete party outfit
                ],
                'color_style': 'bold',  # Complementary, triadic
                'formality': 0.5
            },
            'date': {
                'preferred_combinations': [
                    ('dress',),                   # Date dress
                    ('top', 'bottom'),            # Nice top + pants/skirt
                    ('blazer', 'top', 'bottom'),  # Smart casual
                ],
                'color_style': 'harmonious',  # Analogous colors
                'formality': 0.6
            },
            'sports': {
                'preferred_combinations': [
                    ('top', 'bottom'),            # Athletic top + pants/shorts
                    ('top', 'bottom', 'shoes'),  # Complete sports outfit
                ],
                'color_style': 'vibrant',  # Any colors OK
                'formality': 0.2
            }
        }
        
        print("✅ Outfit Recommender initialized with ML-powered matching")
    
    def recommend_outfits(
        self,
        clothing_items: List[Dict],
        occasion: str,
        max_outfits: int = 5,
        items_per_outfit: int = 2
    ) -> List[Dict]:
        """
        Generate intelligent outfit recommendations
        
        Args:
            clothing_items: List of items with:
                {
                    'id': str,
                    'type': str,
                    'colors': List[dict],
                    'dominant_color': str,
                    'features': np.ndarray,
                    'url': str
                }
            occasion: Occasion type
            max_outfits: Maximum number of outfits to generate
            items_per_outfit: Target items per outfit
        
        Returns:
            List of outfit recommendations with scores
        """
        if not clothing_items:
            return []
        
        # Get occasion rules
        rules = self.occasion_rules.get(occasion, self.occasion_rules['casual'])
        
        # Group items by type
        items_by_type = {}
        for item in clothing_items:
            item_type = item.get('type', 'other')
            if item_type not in items_by_type:
                items_by_type[item_type] = []
            items_by_type[item_type].append(item)
        
        # Generate outfit combinations
        outfits = []
        
        # Try each preferred combination pattern
        for combination in rules['preferred_combinations']:
            generated = self._generate_combinations(
                items_by_type,
                combination,
                occasion,
                rules,
                max_outfits - len(outfits)
            )
            outfits.extend(generated)
            
            if len(outfits) >= max_outfits:
                break
        
        # Sort by score (descending)
        outfits.sort(key=lambda x: x['score'], reverse=True)
        
        return outfits[:max_outfits]
    
    def _generate_combinations(
        self,
        items_by_type: Dict[str, List[Dict]],
        combination_pattern: Tuple[str, ...],
        occasion: str,
        rules: Dict,
        max_combinations: int
    ) -> List[Dict]:
        """
        Generate outfit combinations for a specific pattern
        
        Args:
            items_by_type: Items grouped by type
            combination_pattern: Tuple of types (e.g., ('top', 'bottom'))
            occasion: Occasion type
            rules: Occasion-specific rules
            max_combinations: Maximum combinations to generate
        
        Returns:
            List of outfit dictionaries
        """
        outfits = []
        
        # Check if we have all required types
        available_types = set(items_by_type.keys())
        required_types = set(combination_pattern)
        
        if not required_types.issubset(available_types):
            return outfits
        
        # VALIDATION: Ensure no duplicate clothing types in pattern
        # This prevents recommending top+top or bottom+bottom
        if len(combination_pattern) != len(set(combination_pattern)):
            print(f"⚠️  Warning: Skipping invalid pattern with duplicates: {combination_pattern}")
            return outfits
        
        # VALIDATION: Ensure complementary pieces for proper outfits
        # Must have either: (top + bottom), (dress), or (blazer + top + bottom)
        pattern_set = set(combination_pattern)
        valid_outfit = False
        
        # Single dress is valid
        if pattern_set == {'dress'}:
            valid_outfit = True
        # Top + bottom is valid (shirt + pants)
        elif 'top' in pattern_set and 'bottom' in pattern_set:
            valid_outfit = True
        # Blazer + top + bottom is valid (jacket + shirt + pants)
        elif 'blazer' in pattern_set and 'top' in pattern_set and 'bottom' in pattern_set:
            valid_outfit = True
        # Blazer + dress is valid
        elif 'blazer' in pattern_set and 'dress' in pattern_set:
            valid_outfit = True
        # Shoes can be added to any valid combo
        if 'shoes' in pattern_set:
            shoes_removed = pattern_set - {'shoes'}
            if ('top' in shoes_removed and 'bottom' in shoes_removed) or \
               ('dress' in shoes_removed) or \
               ('blazer' in shoes_removed and 'top' in shoes_removed and 'bottom' in shoes_removed):
                valid_outfit = True
        
        if not valid_outfit:
            print(f"⚠️  Warning: Skipping incomplete outfit pattern: {combination_pattern}")
            return outfits
        
        # Generate combinations recursively
        def generate_recursive(pattern_index: int, current_outfit: List[Dict], used_types: set):
            if pattern_index >= len(combination_pattern):
                # Complete outfit - validate once more
                outfit_types = [item.get('type') for item in current_outfit]
                
                # FINAL VALIDATION: No duplicate types in actual outfit
                if len(outfit_types) != len(set(outfit_types)):
                    return  # Skip outfit with duplicate types
                
                # Calculate score
                score = self._calculate_outfit_score(current_outfit, occasion, rules)
                
                # Get color scheme information for this outfit
                color_scheme_info = self._get_outfit_color_scheme(current_outfit)
                
                # Only add outfits with reasonable scores
                if score >= 0.50:  # Minimum threshold
                    outfits.append({
                        'items': current_outfit.copy(),
                        'score': score,
                        'total_items': len(current_outfit),
                        'occasion': occasion,
                        'types': outfit_types,  # Track types for debugging
                        'color_scheme': color_scheme_info['scheme'],
                        'color_scheme_confidence': color_scheme_info['confidence'],
                        'dominant_colors': color_scheme_info['colors']
                    })
                return
            
            if len(outfits) >= max_combinations:
                return
            
            # Get items for current type
            current_type = combination_pattern[pattern_index]
            
            # VALIDATION: Skip if this type is already used
            if current_type in used_types:
                return
            
            available_items = items_by_type.get(current_type, [])
            
            # Try each item of this type
            for item in available_items[:5]:  # Limit to top 5 per type
                if len(outfits) >= max_combinations:
                    break
                
                # Verify item type matches (double-check classification)
                if item.get('type') != current_type:
                    continue
                
                current_outfit.append(item)
                used_types.add(current_type)
                generate_recursive(pattern_index + 1, current_outfit, used_types)
                used_types.remove(current_type)
                current_outfit.pop()
        
        # Start generation with empty used types set
        generate_recursive(0, [], set())
        
        return outfits
    
    def _calculate_outfit_score(
        self,
        outfit_items: List[Dict],
        occasion: str,
        rules: Dict
    ) -> float:
        """
        Calculate comprehensive outfit score (0-1)
        
        Scoring factors:
        1. Color harmony (40%)
        2. Style similarity (30%)
        3. Occasion appropriateness (20%)
        4. Item variety (10%)
        
        Args:
            outfit_items: List of items in outfit
            occasion: Occasion type
            rules: Occasion rules
        
        Returns:
            Score (0-1)
        """
        if not outfit_items:
            return 0.0
        
        # 1. Color Harmony Score (40%)
        color_score = self._calculate_color_harmony(outfit_items, rules['color_style'])
        
        # 2. Style Similarity Score (30%)
        style_score = self._calculate_style_similarity(outfit_items)
        
        # 3. Occasion Appropriateness (20%)
        occasion_score = self._calculate_occasion_fit(outfit_items, rules)
        
        # 4. Item Variety Score (10%)
        variety_score = len(outfit_items) / 3.0  # 3 items = perfect variety
        variety_score = min(variety_score, 1.0)
        
        # Weighted average
        total_score = (
            color_score * 0.40 +
            style_score * 0.30 +
            occasion_score * 0.20 +
            variety_score * 0.10
        )
        
        return total_score
    
    def _calculate_color_harmony(
        self,
        outfit_items: List[Dict],
        color_style: str
    ) -> float:
        """
        Calculate improved color harmony score for outfit using advanced color theory
        
        Args:
            outfit_items: List of items
            color_style: Style preference from occasion rules
        
        Returns:
            Harmony score (0-1)
        """
        if len(outfit_items) < 2:
            return 0.88  # Single item - good default score
        
        # Get dominant colors from each item
        colors = []
        color_schemes = []
        
        for item in outfit_items:
            dominant = item.get('dominant_color', '#808080')
            colors.append(dominant)
            
            # Get all colors if available for better analysis
            item_colors = item.get('colors', [])
            if item_colors and len(item_colors) > 1:
                # Consider secondary color too
                secondary = item_colors[1]['hex']
                colors.append(secondary)
        
        # Calculate pairwise harmony scores
        harmony_scores = []
        scheme_types = []
        
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                score = self.color_analyzer.are_colors_harmonious(colors[i], colors[j])
                harmony_scores.append(score)
                
                # Track scheme type
                scheme = self.color_analyzer.get_color_scheme_type(colors[i], colors[j])
                scheme_types.append(scheme)
        
        if not harmony_scores:
            return 0.88
        
        # Calculate average harmony
        avg_harmony = np.mean(harmony_scores)
        
        # Adjust based on color style preference
        if color_style == 'conservative':
            # Prefer analogous and monochromatic (subtle)
            if 'analogous' in scheme_types or 'monochromatic' in scheme_types:
                avg_harmony = min(avg_harmony * 1.08, 1.0)
            # Penalize bold complementary
            if 'complementary' in scheme_types and avg_harmony > 0.92:
                avg_harmony *= 0.96
        
        elif color_style == 'bold':
            # Reward complementary and triadic (high contrast)
            if 'complementary' in scheme_types:
                avg_harmony = min(avg_harmony * 1.10, 1.0)
            if 'triadic' in scheme_types:
                avg_harmony = min(avg_harmony * 1.08, 1.0)
        
        elif color_style == 'professional':
            # Prefer neutral combinations
            if 'neutral' in scheme_types:
                avg_harmony = min(avg_harmony * 1.12, 1.0)
            # Bonus for monochromatic professional looks
            if 'monochromatic' in scheme_types:
                avg_harmony = min(avg_harmony * 1.06, 1.0)
        
        elif color_style == 'harmonious':
            # Prefer analogous (soft, romantic)
            if 'analogous' in scheme_types:
                avg_harmony = min(avg_harmony * 1.10, 1.0)
            # Also good: monochromatic
            if 'monochromatic' in scheme_types:
                avg_harmony = min(avg_harmony * 1.08, 1.0)
        
        elif color_style == 'vibrant':
            # Reward any strong color combinations
            if 'triadic' in scheme_types or 'tetradic' in scheme_types:
                avg_harmony = min(avg_harmony * 1.08, 1.0)
        
        # Bonus for variety (not all same scheme)
        unique_schemes = len(set(scheme_types))
        if unique_schemes > 1:
            avg_harmony = min(avg_harmony * 1.03, 1.0)
        
        return float(avg_harmony)
    
    def _calculate_style_similarity(self, outfit_items: List[Dict]) -> float:
        """
        Calculate style similarity using deep learning embeddings
        
        Args:
            outfit_items: List of items with 'features' field
        
        Returns:
            Similarity score (0-1)
        """
        if len(outfit_items) < 2:
            return 0.80
        
        # Get feature vectors
        features_list = []
        for item in outfit_items:
            if 'features' in item and item['features'] is not None:
                features_list.append(item['features'])
        
        if len(features_list) < 2:
            return 0.75  # No features available
        
        # Calculate pairwise cosine similarities
        similarities = []
        
        for i in range(len(features_list)):
            for j in range(i + 1, len(features_list)):
                sim = self.classifier.compute_similarity(
                    features_list[i],
                    features_list[j]
                )
                similarities.append(sim)
        
        if not similarities:
            return 0.75
        
        # Average similarity
        # Higher similarity = more cohesive style
        avg_similarity = np.mean(similarities)
        
        # Normalize to 0.6-1.0 range (avoid too low scores)
        normalized = 0.6 + (avg_similarity * 0.4)
        
        return float(normalized)
    
    def _calculate_occasion_fit(self, outfit_items: List[Dict], rules: Dict) -> float:
        """
        Calculate how well outfit fits the occasion
        
        Args:
            outfit_items: List of items
            rules: Occasion rules
        
        Returns:
            Fit score (0-1)
        """
        formality_required = rules.get('formality', 0.5)
        
        # Calculate outfit formality
        formality_scores = {
            'dress': 0.7,
            'blazer': 0.9,
            'top': 0.5,
            'bottom': 0.5,
            'shoes': 0.6,
            'other': 0.4
        }
        
        outfit_formality = np.mean([
            formality_scores.get(item.get('type', 'other'), 0.5)
            for item in outfit_items
        ])
        
        # Calculate difference from required formality
        formality_diff = abs(outfit_formality - formality_required)
        
        # Convert to score (smaller difference = higher score)
        fit_score = 1.0 - (formality_diff * 0.8)
        fit_score = max(fit_score, 0.5)  # Minimum 0.5
        
        return float(fit_score)
    
    def _get_outfit_color_scheme(self, outfit_items: List[Dict]) -> Dict:
        """
        Determine the dominant color scheme for an outfit
        
        Args:
            outfit_items: List of items in the outfit
        
        Returns:
            Dictionary with scheme type, confidence, and colors
        """
        if len(outfit_items) < 2:
            dominant_color = outfit_items[0].get('dominant_color', '#808080') if outfit_items else '#808080'
            return {
                'scheme': 'monochromatic',
                'confidence': 0.90,
                'colors': [dominant_color]
            }
        
        # Get dominant colors
        colors = [item.get('dominant_color', '#808080') for item in outfit_items]
        
        # Track scheme types from pairwise comparisons
        scheme_counts = {}
        
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                scheme = self.color_analyzer.get_color_scheme_type(colors[i], colors[j])
                scheme_counts[scheme] = scheme_counts.get(scheme, 0) + 1
        
        # Find most common scheme
        if not scheme_counts:
            return {
                'scheme': 'custom',
                'confidence': 0.50,
                'colors': colors
            }
        
        dominant_scheme = max(scheme_counts, key=scheme_counts.get)
        total_pairs = sum(scheme_counts.values())
        confidence = scheme_counts[dominant_scheme] / total_pairs
        
        return {
            'scheme': dominant_scheme,
            'confidence': float(confidence),
            'colors': colors
        }
    
    def _is_neutral_color(self, hex_color: str) -> bool:
        """
        Check if color is neutral (black, white, gray, beige)
        
        Args:
            hex_color: Hex color code
        
        Returns:
            True if neutral
        """
        rgb = self.color_analyzer.hex_to_rgb(hex_color)
        h, s, v = self.color_analyzer.rgb_to_hsv(rgb)
        
        # Low saturation = neutral
        if s < 20:
            return True
        
        # Beige/tan colors (low saturation, warm hue)
        if s < 40 and 20 <= h <= 60:
            return True
        
        return False


# Global recommender instance
_recommender = None

def get_outfit_recommender() -> OutfitRecommender:
    """Get or create global outfit recommender instance"""
    global _recommender
    if _recommender is None:
        _recommender = OutfitRecommender()
    return _recommender
