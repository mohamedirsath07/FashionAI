"""
Test Color Extraction and Naming System
Tests the enhanced color analyzer with naming and schemes
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from color_analyzer import ColorAnalyzer


def test_color_naming():
    """Test color naming system"""
    print("=" * 60)
    print("Testing Color Naming System")
    print("=" * 60)
    
    analyzer = ColorAnalyzer()
    
    test_colors = [
        ("#FF0000", "red"),
        ("#0000FF", "blue"),
        ("#00FF00", "green"),
        ("#FFFF00", "yellow"),
        ("#FF00FF", "magenta"),
        ("#FFA500", "orange"),
        ("#800080", "purple"),
        ("#FFC0CB", "pink"),
        ("#000000", "black"),
        ("#FFFFFF", "white"),
        ("#808080", "gray"),
        ("#A52A2A", "brown"),
        ("#F5F5DC", "beige"),
        ("#000080", "navy"),
        ("#800000", "maroon"),
    ]
    
    passed = 0
    failed = 0
    
    for hex_color, expected_family in test_colors:
        name = analyzer.get_color_name(hex_color)
        print(f"  {hex_color} → {name}")
        
        # Check if the name contains the expected color family
        if expected_family.lower() in name.lower():
            passed += 1
        else:
            failed += 1
            print(f"    ⚠️  Expected '{expected_family}' family")
    
    print(f"\n✅ Passed: {passed}/{len(test_colors)}")
    print(f"❌ Failed: {failed}/{len(test_colors)}")
    print()


def test_color_schemes():
    """Test color scheme generation"""
    print("=" * 60)
    print("Testing Color Schemes")
    print("=" * 60)
    
    analyzer = ColorAnalyzer()
    
    test_color = "#3B5998"  # Blue
    
    schemes = analyzer.get_all_color_schemes(test_color)
    
    print(f"Base Color: {test_color} ({analyzer.get_color_name(test_color)})")
    print()
    
    for scheme_name, colors in schemes.items():
        print(f"  {scheme_name.upper()}:")
        for i, color in enumerate(colors, 1):
            name = analyzer.get_color_name(color)
            print(f"    {i}. {color} - {name}")
        print()
    
    print(f"✅ Generated {len(schemes)} color schemes")
    print()


def test_color_harmony():
    """Test color harmony scoring"""
    print("=" * 60)
    print("Testing Color Harmony Scoring")
    print("=" * 60)
    
    analyzer = ColorAnalyzer()
    
    test_pairs = [
        ("#FF0000", "#00FF00", "Complementary (red-green)"),
        ("#0000FF", "#FFA500", "Complementary (blue-orange)"),
        ("#FF0000", "#FF4500", "Analogous (red-orange red)"),
        ("#0000FF", "#000080", "Monochromatic (blue-navy)"),
        ("#000000", "#FFFFFF", "Neutral (black-white)"),
        ("#808080", "#FF0000", "Neutral + color (gray-red)"),
        ("#FF0000", "#0000FF", "Triadic (red-blue)"),
    ]
    
    for color1, color2, description in test_pairs:
        score = analyzer.are_colors_harmonious(color1, color2)
        scheme = analyzer.get_color_scheme_type(color1, color2)
        name1 = analyzer.get_color_name(color1)
        name2 = analyzer.get_color_name(color2)
        
        print(f"  {description}")
        print(f"    {color1} ({name1}) + {color2} ({name2})")
        print(f"    Scheme: {scheme}, Score: {score:.2f}")
        print()
    
    print("✅ Harmony scoring complete")
    print()


def test_scheme_identification():
    """Test color scheme type identification"""
    print("=" * 60)
    print("Testing Color Scheme Identification")
    print("=" * 60)
    
    analyzer = ColorAnalyzer()
    
    # Test all scheme types
    test_cases = [
        ("#FF0000", "#00FFFF", "complementary"),  # Red-Cyan (180°)
        ("#FF0000", "#FF4500", "analogous"),      # Red-OrangeRed (30°)
        ("#FF0000", "#0000FF", "triadic"),        # Red-Blue (120°)
        ("#0000FF", "#000080", "monochromatic"),  # Blue-Navy (same hue)
        ("#808080", "#A0A0A0", "neutral"),        # Gray-LightGray
    ]
    
    passed = 0
    failed = 0
    
    for color1, color2, expected_scheme in test_cases:
        detected = analyzer.get_color_scheme_type(color1, color2)
        name1 = analyzer.get_color_name(color1)
        name2 = analyzer.get_color_name(color2)
        
        status = "✅" if detected == expected_scheme else "❌"
        print(f"  {status} {color1} ({name1}) + {color2} ({name2})")
        print(f"      Expected: {expected_scheme}, Got: {detected}")
        
        if detected == expected_scheme:
            passed += 1
        else:
            failed += 1
    
    print(f"\n✅ Passed: {passed}/{len(test_cases)}")
    print(f"❌ Failed: {failed}/{len(test_cases)}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("COLOR ANALYZER ENHANCED FEATURES TEST")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Color Naming
        test_color_naming()
        
        # Test 2: Color Schemes
        test_color_schemes()
        
        # Test 3: Harmony Scoring
        test_color_harmony()
        
        # Test 4: Scheme Identification
        test_scheme_identification()
        
        print("=" * 60)
        print("⭐ ALL COLOR TESTS COMPLETED ⭐")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
