"""
Manual testing script for Bharat Context-Adaptive Engine
Run this script to test the inference engine interactively
"""

from inference_engine_enhanced import get_enhanced_inference_engine
from models import RawSignals, DeviceClass, NetworkType, TimeOfDay


def print_separator():
    print("\n" + "=" * 80 + "\n")


def test_scenario(name: str, signals: RawSignals):
    """Test a scenario and print results"""
    print(f"\n{'='*80}")
    print(f"TEST SCENARIO: {name}")
    print(f"{'='*80}\n")
    
    engine = get_enhanced_inference_engine()
    
    print("Running inference...")
    result = engine.infer(signals)
    
    print(f"\n✅ INFERENCE RESULT:")
    print(f"   User Need State: {result.user_need_state}")
    print(f"   Confidence: {result.confidence:.2f}/10.0")
    print(f"   UI Mode: {result.ui_mode.value}")
    print(f"   Language Preference: {result.language_preference.value}")
    
    print(f"\n📋 RECOMMENDED ACTIONS:")
    for i, action in enumerate(result.recommended_actions, 1):
        print(f"   {i}. {action}")
    
    print(f"\n📝 EXPLANATION:")
    print(f"   {result.explanation[:200]}...")
    
    # Get detailed explanation
    inference_id = list(engine.explanations.keys())[-1]
    explanation = engine.get_explanation(inference_id)
    
    if explanation:
        print(f"\n🔍 DETAILED EXPLANATION:")
        print(f"   Signal Count: {explanation.signal_count}")
        print(f"   Signal Categories: {', '.join(explanation.signal_categories)}")
        print(f"   Web Intelligence Applied: {explanation.web_intelligence_applied}")
        print(f"   App Context Applied: {explanation.app_context_applied}")
        print(f"   LLM Reasoning Applied: {explanation.llm_reasoning_applied}")
        print(f"   Total Events: {len(explanation.events)}")
        
        if explanation.decision_factors:
            print(f"\n   Key Decision Factors:")
            for factor in explanation.decision_factors[:5]:
                print(f"     - {factor}")
        
        print(f"\n   Full Explanation:\n")
        print(explanation.generate_human_readable())
    
    print_separator()


def main():
    """Run manual tests"""
    print("\n" + "="*80)
    print("BHARAT CONTEXT-ADAPTIVE ENGINE - MANUAL TESTING")
    print("="*80)
    
    # Test 1: Morning Devotional User
    test_scenario(
        "Morning Devotional User",
        RawSignals(
            time_of_day=TimeOfDay.MORNING,
            hour_of_day=7,
            system_language="hi",
            first_action="voice",
            festival_day="diwali",
            whatsapp_installed="yes"
        )
    )
    
    # Test 2: Evening Ledger User (Enhanced)
    test_scenario(
        "Evening Ledger / Business User (Enhanced)",
        RawSignals(
            time_of_day=TimeOfDay.EVENING,
            hour_of_day=19,
            business_apps=["khatabook", "okcredit"],
            whatsapp_business_usage="yes",
            payment_apps_installed=["paytm", "phonepe", "gpay"],
            otp_message_frequency="high",
            banking_sms_presence="yes",
            system_language="hi",
            city_tier="tier3",
            day_of_week="monday"
        )
    )
    
    # Test 3: Student Exam User
    test_scenario(
        "Student Exam Time User",
        RawSignals(
            education_apps=["byjus", "unacademy"],
            session_duration="long",
            text_input_length="long",
            total_notification_volume="low",
            time_of_day=TimeOfDay.AFTERNOON,
            hour_of_day=14,
            return_user="yes",
            device_class=DeviceClass.MID_RANGE
        )
    )
    
    # Test 4: Low-network Slow Device User
    test_scenario(
        "Low-network Slow Device User",
        RawSignals(
            device_class=DeviceClass.LOW_END,
            network_type=NetworkType.THREE_G,
            network_speed="slow",
            ram_size="2GB",
            connection_stability="unstable",
            data_saver_mode="enabled",
            app_launch_time="slow"
        )
    )
    
    # Test 5: WhatsApp Business User
    test_scenario(
        "WhatsApp Business User",
        RawSignals(
            whatsapp_installed="yes",
            whatsapp_active="yes",
            whatsapp_business_usage="yes",
            whatsapp_group_activity="high",
            whatsapp_notification_frequency="high",
            business_apps=["khatabook"],
            payment_apps_installed=["paytm", "phonepe"],
            system_language="hi"
        )
    )
    
    # Test 6: High OTP Frequency User
    test_scenario(
        "High OTP / Transaction User",
        RawSignals(
            otp_message_frequency="high",
            banking_sms_presence="yes",
            ecommerce_sms_presence="yes",
            payment_apps_installed=["paytm", "phonepe", "gpay"],
            banking_apps="yes",
            sms_response_time="immediate",
            system_language="hi"
        )
    )
    
    # Test 7: Minimal Signals (Default)
    test_scenario(
        "Minimal Signals (Default Fallback)",
        RawSignals(
            device_class=DeviceClass.MID_RANGE
        )
    )
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

