"""
Test script for Small Vendor Persona using API
Runs inference and generates recommendations for Day-0, Day-1, Day-7
"""

import json
import requests
from pathlib import Path


def load_signals():
    """Load small vendor signals from JSON file"""
    signals_file = Path(__file__).parent / "small_vendor_signals.json"
    with open(signals_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["signals"]


def main():
    """Main test function"""
    print("=" * 80)
    print("SMALL VENDOR PERSONA - INFERENCE & RECOMMENDATIONS TEST")
    print("=" * 80)
    print()
    
    # Load signals
    print("📊 Loading 50 signals for Small Vendor persona...")
    signals = load_signals()
    signal_count = len([v for v in signals.values() if v is not None])
    print(f"✅ Loaded {signal_count} signals")
    print()
    
    base_url = "http://localhost:8000"
    
    # Step 1: Run inference
    print("🔍 Step 1: Running Enhanced Inference Engine...")
    print("-" * 80)
    try:
        inference_response = requests.post(
            f"{base_url}/v1/infer",
            json={"signals": signals},
            params={"enhanced": True}
        )
        inference_response.raise_for_status()
        inference_data = inference_response.json()
        
        if inference_data["success"]:
            inference = inference_data["data"]
            print(f"✅ User Need State: {inference['user_need_state']}")
            print(f"📈 Confidence: {inference['confidence']}/10.0")
            print(f"🎨 UI Mode: {inference['ui_mode']}")
            print(f"🌐 Language: {inference['language_preference']}")
            print(f"📋 Matched Signals: {len(inference['matched_signals'])}")
            print()
            print("📝 Recommended Actions:")
            for i, action in enumerate(inference['recommended_actions'], 1):
                print(f"  {i}. {action}")
            print()
        else:
            print(f"❌ Error: {inference_data.get('error')}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        print("Make sure the server is running: python main.py")
        return
    
    # Step 2: Generate recommendations for all days
    print("=" * 80)
    print("🎯 Step 2: GENERATING RECOMMENDATIONS")
    print("=" * 80)
    print()
    
    try:
        recommendations_response = requests.post(
            f"{base_url}/v1/recommendations/all-days",
            json={"signals": signals},
            params={"enhanced": True}
        )
        recommendations_response.raise_for_status()
        rec_data = recommendations_response.json()
        
        if rec_data["success"]:
            recommendations = rec_data["recommendations"]
            
            # Day-0 Recommendations
            print("📅 DAY-0: Home Page Personalization")
            print("-" * 80)
            day_0 = recommendations["day_0"]
            print(f"Outcome: {day_0['outcome']}")
            print(f"Delivery: {day_0['delivery_medium']}")
            print(f"Timing: {day_0['timing']['when']}")
            print()
            print("Content:")
            content = day_0['content']
            print(f"  Hero Prompt: {content['hero_section']['prompt']}")
            print(f"  Language: {content['hero_section']['language']}")
            print(f"  Quick Actions: {', '.join(content['quick_actions'][:4])}")
            print(f"  Example Prompts:")
            for prompt in content['example_prompts'][:3]:
                print(f"    • {prompt}")
            print()
            
            # Day-1 Recommendations
            print("📅 DAY-1: Engagement (Push Notifications, Reminders, Daily Summaries)")
            print("-" * 80)
            day_1 = recommendations["day_1"]
            print(f"Outcome: {day_1['outcome']}")
            print(f"Delivery: {', '.join(day_1['delivery_medium'])}")
            print()
            print("Push Notifications:")
            for notif in day_1['content']['push_notifications']:
                print(f"  • {notif['title']}")
                print(f"    {notif['body']}")
                print(f"    Time: {notif['time']}")
            print()
            print("Reminders:")
            for reminder in day_1['content']['reminders']:
                print(f"  • {reminder['message']} (Time: {reminder['time']})")
            print()
            print("Daily Summaries:")
            for summary in day_1['content']['daily_summaries']:
                print(f"  • {summary['title']}")
                print(f"    {summary['content']}")
            print()
            
            # Day-7 Recommendations
            print("📅 DAY-7: Retention & Growth (Weekly Insights, Feature Suggestions)")
            print("-" * 80)
            day_7 = recommendations["day_7"]
            print(f"Outcome: {day_7['outcome']}")
            print(f"Delivery: {', '.join(day_7['delivery_medium'])}")
            print()
            print("Weekly Insights:")
            for insight in day_7['content']['weekly_insights']:
                print(f"  • {insight['title']}")
                print(f"    {insight['content']}")
            print()
            print("Feature Suggestions:")
            for feature in day_7['content']['feature_suggestions']:
                print(f"  • {feature}")
            print()
            
            # Save results
            results = {
                "inference": inference,
                "recommendations": recommendations
            }
            
            output_file = Path(__file__).parent / "small_vendor_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print("=" * 80)
            print(f"✅ Results saved to: {output_file}")
            print("=" * 80)
        else:
            print(f"❌ Error: {rec_data.get('error')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        print("Make sure the server is running: python main.py")


if __name__ == "__main__":
    main()

