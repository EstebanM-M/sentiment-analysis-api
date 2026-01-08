"""
Manual API testing script
Test the API endpoints with sample requests
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import requests
import json
from pprint import pprint

# API base URL
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_health():
    """Test health check endpoint"""
    print_section("HEALTH CHECK")
    
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"Status: {response.status_code}")
    print(f"Response:")
    pprint(response.json())

def test_single_analysis():
    """Test single text analysis"""
    print_section("SINGLE TEXT ANALYSIS")
    
    test_cases = [
        "I love this product! It's amazing and works perfectly.",
        "This is terrible. Worst purchase ever.",
        "It's okay, nothing special really.",
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: \"{text[:50]}...\"")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze",
            json={"text": text}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Label: {data['label']}")
            print(f"   Score: {data['score']:.4f} ({data['score']*100:.2f}%)")
        else:
            print(f"   Error: {response.status_code}")
            print(f"   {response.json()}")

def test_batch_analysis():
    """Test batch analysis"""
    print_section("BATCH ANALYSIS")
    
    texts = [
        "Excellent service!",
        "Terrible experience.",
        "Pretty good overall.",
        "I hate this.",
        "Love it!"
    ]
    
    print(f"Analyzing {len(texts)} texts...")
    
    response = requests.post(
        f"{BASE_URL}/api/v1/batch-analyze",
        json={"texts": texts}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal analyzed: {data['total_analyzed']}")
        print(f"Processing time: {data['processing_time_ms']:.2f}ms")
        print(f"\nResults:")
        
        for i, result in enumerate(data['results'], 1):
            print(f"{i}. \"{result['text'][:40]}...\"")
            print(f"   → {result['label']} ({result['score']:.4f})")
    else:
        print(f"Error: {response.status_code}")
        pprint(response.json())

def test_model_info():
    """Test model info endpoint"""
    print_section("MODEL INFORMATION")
    
    response = requests.get(f"{BASE_URL}/api/v1/model-info")
    print(f"Status: {response.status_code}")
    print("Response:")
    pprint(response.json())

def test_error_cases():
    """Test error handling"""
    print_section("ERROR HANDLING")
    
    # Test empty text
    print("1. Testing empty text:")
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json={"text": ""}
    )
    print(f"   Status: {response.status_code} (expected: 422)")
    
    # Test missing field
    print("\n2. Testing missing text field:")
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json={}
    )
    print(f"   Status: {response.status_code} (expected: 422)")
    
    # Test empty batch
    print("\n3. Testing empty batch:")
    response = requests.post(
        f"{BASE_URL}/api/v1/batch-analyze",
        json={"texts": []}
    )
    print(f"   Status: {response.status_code} (expected: 422)")

def main():
    """Run all tests"""
    print("\n🧪 TESTING SENTIMENT ANALYSIS API")
    print(f"📍 Base URL: {BASE_URL}")
    
    try:
        # Check if API is running
        response = requests.get(BASE_URL, timeout=2)
        if response.status_code != 200:
            print("\n❌ API is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API")
        print("   Make sure the API is running:")
        print("   python run_api.py")
        return
    
    # Run tests
    test_health()
    test_model_info()
    test_single_analysis()
    test_batch_analysis()
    test_error_cases()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)
    print(f"\n📚 View full API documentation at: {BASE_URL}/docs")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
