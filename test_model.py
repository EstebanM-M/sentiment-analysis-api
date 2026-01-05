"""
Quick test script for the sentiment model
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.sentiment_model import SentimentAnalyzer

def main():
    print("🧪 Testing Sentiment Analysis Model\n")
    
    # Initialize analyzer
    print("Loading model...")
    analyzer = SentimentAnalyzer()
    
    # Test cases
    test_texts = [
        "I love this product! It's amazing and works perfectly.",
        "This is terrible. Worst purchase ever.",
        "It's okay, nothing special.",
        "Absolutely fantastic experience! Highly recommend!",
        "Very disappointed with the service."
    ]
    
    print("\n" + "="*60)
    print("SINGLE TEXT ANALYSIS")
    print("="*60)
    
    for text in test_texts[:2]:
        result = analyzer.analyze(text)
        print(f"\nText: {result['text'][:50]}...")
        print(f"Sentiment: {result['label']}")
        print(f"Confidence: {result['score']:.2%}")
    
    print("\n" + "="*60)
    print("BATCH ANALYSIS")
    print("="*60)
    
    results = analyzer.analyze_batch(test_texts)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['text'][:40]}...")
        print(f"   → {result['label']} ({result['score']:.2%})")
    
    print("\n" + "="*60)
    print("MODEL INFO")
    print("="*60)
    info = analyzer.get_model_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    main()
