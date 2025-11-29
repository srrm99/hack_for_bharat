
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_service import LLMService
from src.models import RawSignals

def verify_apis():
    print("\n=== Verifying Real API Connectivity ===\n")
    
    # Load env vars
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
    
    service = LLMService()
    
    # 1. Check Keys
    print(f"OpenRouter Key Present: {'✅' if service.openrouter_key else '❌'}")
    print(f"Perplexity Key Present: {'✅' if service.perplexity_key else '❌'}")
    print("-" * 50)

    if not service.openrouter_key and not service.perplexity_key:
        print("⚠️  No API keys found. Please add them to .env file.")
        return

    # 2. Test Perplexity (Web Intelligence)
    if service.perplexity_key:
        print("\nTesting Perplexity API (Web Intelligence)...")
        try:
            response = service.get_web_intelligence("What is the current time in India?")
            print(f"✅ Perplexity Response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Perplexity Failed: {e}")
    
    # 3. Test OpenRouter (LLM Reasoning)
    if service.openrouter_key:
        print("\nTesting OpenRouter API (Reasoning)...")
        try:
            # Create dummy signals
            signals = RawSignals(
                device_class="mid_range",
                time_of_day="evening",
                business_apps=["khatabook"],
                system_language="hi"
            )
            
            print("Sending signal payload for reasoning...")
            result = service.infer_user_profile_with_reasoning(signals, "Context: User has business apps")
            
            if "error" in result:
                print(f"❌ OpenRouter Failed: {result['error']}")
            else:
                print("✅ OpenRouter Response Received!")
                print(f"Inferred State: {result.get('user_need_state')}")
                print(f"Reasoning: {result.get('reasoning_summary')}")
                
        except Exception as e:
            print(f"❌ OpenRouter Failed: {e}")

if __name__ == "__main__":
    verify_apis()

