"""
Simple import test for the sentiment model
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Testing imports...")

try:
    from models.sentiment_model import SentimentAnalyzer, get_analyzer
    print("✅ Models imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

try:
    from transformers import pipeline
    print("✅ Transformers library available")
except ImportError:
    print("❌ Transformers not available")
    sys.exit(1)

print("\n🎉 All imports successful! Ready for model testing.")
print("\nNote: To run the full model test, you'll need PyTorch installed:")
print("  pip install torch --index-url https://download.pytorch.org/whl/cpu")
