
import requests
import json
import os
import sys

# Add the parent directory to path to import from examples if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_inference_flow():
    print("\n=== Testing Bharat Context-Adaptive Engine Workflow ===\n")
    
    # Load signal data
    signals_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples", "small_vendor_signals.json")
    with open(signals_path, 'r') as f:
        data = json.load(f)
    
    signals = data["signals"]
    print(f"loaded signals for: {signals.get('business_apps')} in {signals.get('state')} ({signals.get('system_language')})")
    
    # API Endpoint (assuming running locally)
    url = "http://127.0.0.1:8000/v1/infer"
    
    print(f"Sending request to {url}...")
    
    try:
        response = requests.post(url, json={"signals": signals})
        response.raise_for_status()
        result = response.json()
        
        if result["success"]:
            data = result["data"]
            print("\n✅ Inference Successful!")
            print("-" * 50)
            print(f"User Need State:  {data['user_need_state']}")
            print(f"Confidence:       {data['confidence']}/10")
            print(f"UI Mode:          {data['ui_mode']}")
            print(f"Language:         {data['language_preference']}")
            print("-" * 50)
            print("Recommended Actions:")
            for action in data['recommended_actions']:
                print(f"  - {action}")
            print("-" * 50)
            print("Explanation:")
            print(data['explanation'])
            print("-" * 50)
            
            # Check if reasoning was used
            if "Reasoning" in data['explanation'] or "LLM" in data['explanation']:
                print("🧠 LLM/Reasoning logic was applied.")
            else:
                print("ℹ️  Rule-based logic was applied (add API keys for LLM reasoning).")
                
        else:
            print("❌ Inference Failed:")
            print(result.get("error"))
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure 'uvicorn main:app --reload' is running in 'src/' directory.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_inference_flow()

