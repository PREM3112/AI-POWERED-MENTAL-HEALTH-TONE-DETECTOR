import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils.mentalbert_handler import mentalbert_analyzer

def test_mentalbert():
    """Test MentalBERT integration"""
    test_cases = [
        "I've been feeling really happy and content with life lately",
        "I can't stop worrying about everything, I feel so anxious",
        "I feel so empty and hopeless, nothing brings me joy anymore",
        "Just a normal day, nothing special to report"
    ]
    
    print("🧪 Testing MentalBERT Integration...")
    print(f"Model loaded: {mentalbert_analyzer.is_loaded}")
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Text: {text}")
        
        result = mentalbert_analyzer.analyze_text(text)
        
        print(f"Primary Tone: {result['primary_tone']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Model Used: {result.get('model_used', 'unknown')}")

if __name__ == '__main__':
    test_mentalbert()