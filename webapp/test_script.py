import requests
import json
import time

def test_speech_functionality():
    base_url = "http://localhost:5000"
    
    print("🎤 Testing Speech Processing...")
    
    try:
        # Test 1: Record audio
        print("1. Recording audio...")
        record_data = {"duration": 5}
        record_response = requests.post(f"{base_url}/record-audio", json=record_data)
        record_result = record_response.json()
        
        print("Recording result:", json.dumps(record_result, indent=2))
        
        if record_result.get('success'):
            # Test 2: Analyze audio
            print("\n2. Analyzing audio...")
            analyze_data = {"filename": record_result['filename']}
            analyze_response = requests.post(f"{base_url}/analyze-audio", json=analyze_data)
            analyze_result = analyze_response.json()
            
            print("Analysis result:")
            print(json.dumps(analyze_result, indent=2))
            
            # Test 3: Check health status
            print("\n3. Checking system health...")
            health_response = requests.get(f"{base_url}/health")
            health_result = health_response.json()
            
            print("Health status:")
            print(json.dumps(health_result, indent=2))
            
            return analyze_result
        
        return None
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    result = test_speech_functionality()
    if result:
        print(f"\n🎉 Speech test completed! Detected emotion: {result.get('emotion', 'unknown')}")
    else:
        print("\n💥 Speech test failed!")