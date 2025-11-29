"""
Test script for Small Vendor Persona
Runs inference and generates recommendations for Day-0, Day-1, Day-7
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add src to path
sys.path.insert(0, str(project_root / "src"))

from models import RawSignals, InferenceRequest
from inference_engine_enhanced import get_enhanced_inference_engine
from recommendation_engine import RecommendationEngine


def load_signals():
    """Load small vendor signals from JSON file"""
    signals_file = Path(__file__).parent / "small_vendor_signals.json"
    with open(signals_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return RawSignals(**data["signals"])


def main():
    """Main test function"""
    print("=" * 80)
    print("SMALL VENDOR PERSONA - INFERENCE & RECOMMENDATIONS TEST")
    print("=" * 80)
    print()
    
    # Load signals
    print("📊 Loading 50 signals for Small Vendor persona...")
    signals = load_signals()
    print(f"✅ Loaded {len([v for v in signals.dict().values() if v is not None])} signals")
    print()
    
    # Run inference
    print("🔍 Running Enhanced Inference Engine...")
    print("-" * 80)
    engine = get_enhanced_inference_engine()
    inference_output = engine.infer(signals)
    
    print(f"✅ User Need State: {inference_output.user_need_state}")
    print(f"📈 Confidence: {inference_output.confidence}/10.0")
    print(f"🎨 UI Mode: {inference_output.ui_mode.value}")
    print(f"🌐 Language: {inference_output.language_preference.value}")
    print(f"📋 Matched Signals: {len(inference_output.matched_signals)}")
    print()
    
    print("📝 Recommended Actions:")
    for i, action in enumerate(inference_output.recommended_actions, 1):
        print(f"  {i}. {action}")
    print()
    
    # Generate recommendations
    print("=" * 80)
    print("🎯 GENERATING RECOMMENDATIONS")
    print("=" * 80)
    print()
    
    recommendation_engine = RecommendationEngine()
    
    # Day-0 Recommendations
    print("📅 DAY-0: Home Page Personalization")
    print("-" * 80)
    day_0 = recommendation_engine.generate_recommendations(inference_output, day=0)
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
    day_1 = recommendation_engine.generate_recommendations(inference_output, day=1)
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
    day_7 = recommendation_engine.generate_recommendations(inference_output, day=7)
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
        "inference": {
            "user_need_state": inference_output.user_need_state,
            "confidence": inference_output.confidence,
            "ui_mode": inference_output.ui_mode.value,
            "language_preference": inference_output.language_preference.value,
            "matched_signals": inference_output.matched_signals,
            "recommended_actions": inference_output.recommended_actions
        },
        "recommendations": {
            "day_0": day_0,
            "day_1": day_1,
            "day_7": day_7
        }
    }
    
    output_file = Path(__file__).parent / "small_vendor_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 80)
    print(f"✅ Results saved to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()

