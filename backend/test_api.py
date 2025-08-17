"""
Test script untuk RAG Anything Assistant API
"""
import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error connecting to API: {str(e)}")
    print("-" * 50)

def test_stats():
    """Test stats endpoint"""
    print("Testing stats endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        if response.status_code == 200:
            print("✅ Stats endpoint working")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print("-" * 50)

def test_chat(question):
    """Test chat endpoint"""
    print(f"Testing chat with question: '{question}'")
    try:
        payload = {"question": question}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat response received")
            print(f"Answer: {result['answer']}")
            print(f"Sources: {result['sources']}")
            return result['timestamp']
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    print("-" * 50)

def test_history(date_str):
    """Test history endpoint"""
    print(f"Testing history for date: {date_str}")
    try:
        response = requests.get(f"{API_BASE_URL}/history/{date_str}")
        if response.status_code == 200:
            result = response.json()
            print("✅ History retrieved")
            print(f"Date: {result['date']}")
            print(f"Conversations: {len(result['conversations'])}")
            for i, conv in enumerate(result['conversations']):
                print(f"  {i+1}. {conv['question'][:50]}...")
        else:
            print(f"❌ History failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print("-" * 50)

def main():
    """Run all tests"""
    print("🚀 Starting RAG Anything Assistant API Tests")
    print("=" * 60)
    
    # Test 1: Health check
    test_health_check()
    
    # Test 2: Stats
    test_stats()
    
    # Test 3: Chat with different questions
    test_questions = [
        "Apa itu FastAPI?",
        "Bagaimana cara implementasi RAG?",
        "Jelaskan tentang Python untuk AI"
    ]
    
    timestamps = []
    for question in test_questions:
        timestamp = test_chat(question)
        if timestamp:
            timestamps.append(timestamp)
    
    # Test 4: History check
    if timestamps:
        # Get today's date for history check
        today = datetime.now().strftime("%Y-%m-%d")
        test_history(today)
    
    print("🏁 All tests completed!")

if __name__ == "__main__":
    main()
