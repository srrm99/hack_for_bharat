"""
Test cases for Bharat Context-Adaptive Engine
"""

import pytest
from datetime import datetime
from models import RawSignals, DeviceClass, NetworkType, TimeOfDay
from inference_engine import InferenceEngine, get_inference_engine


class TestInferenceEngine:
    """Test suite for InferenceEngine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = InferenceEngine()
    
    def test_morning_devotional_user(self):
        """Test inference for morning devotional user"""
        signals = RawSignals(
            time_of_day=TimeOfDay.MORNING,
            hour_of_day=7,
            system_language="hi",
            first_action="voice",
            festival_day="diwali"
        )
        
        result = self.engine.infer(signals)
        
        assert result.user_need_state == "Morning Devotional User"
        assert result.confidence > 0
        assert result.ui_mode.value == "voice-first"
        assert len(result.recommended_actions) >= 3
        assert "devotional" in result.explanation.lower() or "morning" in result.explanation.lower()
    
    def test_evening_ledger_user(self):
        """Test inference for evening ledger/khatabook user"""
        signals = RawSignals(
            time_of_day=TimeOfDay.EVENING,
            hour_of_day=19,
            day_of_week="monday",
            payment_apps_installed=["paytm", "phonepe"],
            city_tier="tier3",
            text_input_length="medium"
        )
        
        result = self.engine.infer(signals)
        
        assert result.user_need_state == "Evening Ledger / Khatabook Mode User"
        assert result.confidence > 0
        assert len(result.recommended_actions) >= 3
    
    def test_low_network_slow_device_user(self):
        """Test inference for low-network slow device user"""
        signals = RawSignals(
            network_type=NetworkType.THREE_G,
            network_speed="slow",
            device_class=DeviceClass.LOW_END,
            ram_size="2GB",
            connection_stability="unstable",
            data_saver_mode="enabled"
        )
        
        result = self.engine.infer(signals)
        
        assert result.user_need_state == "Low-network Slow Device User"
        assert result.confidence > 0
        assert result.ui_mode.value == "lite"
    
    def test_hindi_first_user(self):
        """Test inference for Hindi-first user"""
        signals = RawSignals(
            system_language="hi",
            keyboard_language="hindi",
            state="UP",
            language_region="hindi"
        )
        
        result = self.engine.infer(signals)
        
        assert result.user_need_state == "Hindi-first User"
        assert result.confidence > 0
        assert result.language_preference.value == "hindi"
    
    def test_voice_first_user(self):
        """Test inference for voice-first user"""
        signals = RawSignals(
            first_action="voice",
            voice_button_tapped="yes",
            microphone_permission="granted",
            text_input_length="none",
            keyboard_opened="no"
        )
        
        result = self.engine.infer(signals)
        
        assert result.user_need_state == "Voice-first User"
        assert result.confidence > 0
        assert result.ui_mode.value == "voice-first"
    
    def test_ai_beginner_user(self):
        """Test inference for AI beginner user"""
        signals = RawSignals(
            time_since_install="immediate",
            first_prompt_attempted="no",
            example_prompts_viewed="yes",
            tutorial_started="yes",
            help_faq_opened="yes",
            text_input_length="none"
        )
        
        result = self.engine.infer(signals)
        
        assert result.user_need_state == "AI Beginner / First-time Prompt Explorer"
        assert result.confidence > 0
    
    def test_festival_day_user(self):
        """Test inference for festival day user"""
        signals = RawSignals(
            festival_day="diwali",
            regional_holiday="yes",
            system_language="hi"
        )
        
        result = self.engine.infer(signals)
        
        assert result.user_need_state == "Festival-Day User"
        assert result.confidence > 0
    
    def test_default_rule_fallback(self):
        """Test default rule when no conditions match"""
        signals = RawSignals(
            # Minimal signals that don't match any rule
            device_class=DeviceClass.MID_RANGE
        )
        
        result = self.engine.infer(signals)
        
        # Should fallback to default
        assert result.user_need_state is not None
        assert len(result.recommended_actions) >= 3
    
    def test_extract_signals(self):
        """Test signal extraction from payload"""
        payload = {
            "device_class": "low_end",
            "network_type": "3g",
            "system_language": "hi",
            "hour_of_day": 8,
            "time_of_day": "morning"
        }
        
        signals = self.engine.extract_signals(payload)
        
        assert signals.device_class == DeviceClass.LOW_END
        assert signals.network_type == NetworkType.THREE_G
        assert signals.system_language == "hi"
        assert signals.hour_of_day == 8
    
    def test_score_rules(self):
        """Test rule scoring"""
        signals = RawSignals(
            time_of_day=TimeOfDay.MORNING,
            hour_of_day=7,
            system_language="hi",
            first_action="voice"
        )
        
        rule_scores = self.engine.score_rules(signals)
        
        assert len(rule_scores) > 0
        # Should be sorted by score (descending)
        scores = [score for _, score, _, _ in rule_scores]
        assert scores == sorted(scores, reverse=True)
    
    def test_generate_recommendations(self):
        """Test recommendation generation"""
        signals = RawSignals(
            time_of_day=TimeOfDay.MORNING,
            system_language="hi"
        )
        
        rule_scores = self.engine.score_rules(signals)
        user_need_state, confidence, matched_rule, _, _ = self.engine.infer_need_state(signals, rule_scores)
        
        actions, ui_mode, lang_pref = self.engine.generate_recommendations(
            user_need_state, matched_rule, signals
        )
        
        assert len(actions) >= 3
        assert len(actions) <= 5
        assert ui_mode is not None
        assert lang_pref is not None
    
    def test_generate_explanation(self):
        """Test explanation generation"""
        explanation = self.engine.generate_explanation(
            "Morning Devotional User",
            ["time_of_day", "hour_of_day", "system_language"],
            ["time_of_day=morning", "hour_of_day=7", "system_language=hi"],
            7.5
        )
        
        assert "Morning Devotional User" in explanation
        assert "7.5" in explanation or "7" in explanation
        assert len(explanation) > 0


class TestRuleConditions:
    """Test rule condition evaluation"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = InferenceEngine()
    
    def test_equals_operator(self):
        """Test equals operator"""
        from inference_engine import RuleCondition
        
        condition = RuleCondition({
            "signal": "system_language",
            "operator": "equals",
            "value": "hi",
            "weight": 2.0
        })
        
        matches, score = condition.evaluate("hi")
        assert matches is True
        assert score == 2.0
        
        matches, score = condition.evaluate("en")
        assert matches is False
        assert score == 0.0
    
    def test_in_operator(self):
        """Test in operator"""
        from inference_engine import RuleCondition
        
        condition = RuleCondition({
            "signal": "time_of_day",
            "operator": "in",
            "value": ["morning", "evening"],
            "weight": 1.5
        })
        
        matches, score = condition.evaluate("morning")
        assert matches is True
        assert score == 1.5
        
        matches, score = condition.evaluate("afternoon")
        assert matches is False
        assert score == 0.0
    
    def test_between_operator(self):
        """Test between operator"""
        from inference_engine import RuleCondition
        
        condition = RuleCondition({
            "signal": "hour_of_day",
            "operator": "between",
            "value": [5, 9],
            "weight": 2.0
        })
        
        matches, score = condition.evaluate(7)
        assert matches is True
        assert score == 2.0
        
        matches, score = condition.evaluate(10)
        assert matches is False
        assert score == 0.0
    
    def test_none_value(self):
        """Test condition with None signal value"""
        from inference_engine import RuleCondition
        
        condition = RuleCondition({
            "signal": "system_language",
            "operator": "equals",
            "value": "hi",
            "weight": 2.0
        })
        
        matches, score = condition.evaluate(None)
        assert matches is False
        assert score == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

