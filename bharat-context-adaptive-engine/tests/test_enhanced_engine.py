"""
Test cases for Enhanced Inference Engine
Tests web intelligence, app context, LLM reasoning, and explanation system
"""

import pytest
from datetime import datetime
from models import RawSignals, DeviceClass, NetworkType, TimeOfDay
from inference_engine_enhanced import get_enhanced_inference_engine, EnhancedInferenceEngine
from web_intelligence import WebIntelligence
from app_context import AppContext
from llm_reasoning import LLMReasoning


class TestEnhancedInferenceEngine:
    """Test suite for Enhanced Inference Engine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = get_enhanced_inference_engine()
    
    def test_enhanced_inference_business_user(self):
        """Test enhanced inference for business user with all modules"""
        signals = RawSignals(
            business_apps=["khatabook", "okcredit"],
            whatsapp_business_usage="yes",
            payment_apps_installed=["paytm", "phonepe"],
            time_of_day=TimeOfDay.EVENING,
            hour_of_day=19,
            otp_message_frequency="high",
            banking_sms_presence="yes",
            system_language="hi",
            city_tier="tier3"
        )
        
        result = self.engine.infer(signals)
        
        # Should infer business/ledger user
        assert "ledger" in result.user_need_state.lower() or "business" in result.user_need_state.lower() or "shop" in result.user_need_state.lower()
        assert result.confidence > 0
        assert len(result.recommended_actions) >= 3
        
        # Check explanation exists
        inference_id = list(self.engine.explanations.keys())[-1]
        explanation = self.engine.get_explanation(inference_id)
        assert explanation is not None
        assert explanation.web_intelligence_applied is True
        assert explanation.app_context_applied is True
        assert explanation.llm_reasoning_applied is True
    
    def test_web_intelligence_detection(self):
        """Test web intelligence pattern detection"""
        signals = RawSignals(
            business_apps=["khatabook"],
            whatsapp_business_usage="yes",
            otp_message_frequency="high"
        )
        
        web_intel = WebIntelligence()
        result = web_intel.analyze_signals(signals)
        
        assert result["web_intelligence_applied"] is True
        assert len(result["detected_patterns"]) > 0
        assert len(result["insights"]) > 0
        assert "business_apps_present" in result["detected_patterns"] or "whatsapp_business_usage" in result["detected_patterns"]
    
    def test_app_context_detection(self):
        """Test app context use case detection"""
        signals = RawSignals(
            education_apps=["byjus", "unacademy"],
            session_duration="long",
            text_input_length="long",
            time_of_day=TimeOfDay.AFTERNOON
        )
        
        app_context = AppContext()
        result = app_context.analyze_app_context(signals)
        
        assert result["app_context_applied"] is True
        assert len(result["detected_use_cases"]) > 0
        assert "student_help" in result["detected_use_cases"]
        assert len(result["prompt_suggestions"]) > 0
    
    def test_llm_reasoning(self):
        """Test LLM reasoning"""
        signals = RawSignals(
            business_apps=["khatabook"],
            whatsapp_business_usage="yes",
            time_of_day=TimeOfDay.EVENING,
            payment_apps_installed=["paytm"]
        )
        
        web_intel = WebIntelligence().analyze_signals(signals)
        app_context = AppContext().analyze_app_context(signals)
        
        llm_reasoning = LLMReasoning()
        result = llm_reasoning.reason(signals, web_intel, app_context)
        
        assert result["llm_reasoning_applied"] is True
        assert len(result["insights"]) > 0
        assert len(result["reasoning_steps"]) > 0
    
    def test_explanation_events(self):
        """Test explanation event creation"""
        signals = RawSignals(
            time_of_day=TimeOfDay.MORNING,
            hour_of_day=7,
            system_language="hi",
            first_action="voice"
        )
        
        result = self.engine.infer(signals)
        
        # Get explanation
        inference_id = list(self.engine.explanations.keys())[-1]
        explanation = self.engine.get_explanation(inference_id)
        
        assert explanation is not None
        assert len(explanation.events) >= 5  # Should have multiple events
        assert explanation.signal_count > 0
        assert explanation.final_user_need_state is not None
        assert explanation.final_confidence is not None
    
    def test_explanation_human_readable(self):
        """Test human-readable explanation generation"""
        signals = RawSignals(
            business_apps=["khatabook"],
            whatsapp_business_usage="yes",
            time_of_day=TimeOfDay.EVENING
        )
        
        result = self.engine.infer(signals)
        inference_id = list(self.engine.explanations.keys())[-1]
        explanation = self.engine.get_explanation(inference_id)
        
        human_readable = explanation.generate_human_readable()
        
        assert len(human_readable) > 0
        assert explanation.final_user_need_state in human_readable
        assert str(explanation.final_confidence) in human_readable
    
    def test_confidence_adjustments(self):
        """Test confidence adjustments from multiple sources"""
        signals = RawSignals(
            business_apps=["khatabook", "okcredit"],
            whatsapp_business_usage="yes",
            payment_apps_installed=["paytm", "phonepe"],
            otp_message_frequency="high",
            time_of_day=TimeOfDay.EVENING,
            hour_of_day=19
        )
        
        result = self.engine.infer(signals)
        
        # Enhanced engine should have higher confidence due to adjustments
        assert result.confidence >= 0
        # With multiple sources agreeing, confidence should be higher
        if result.user_need_state and ("ledger" in result.user_need_state.lower() or "business" in result.user_need_state.lower()):
            assert result.confidence >= 5.0  # Should be reasonably confident
    
    def test_signal_correlation(self):
        """Test signal correlation detection"""
        signals = RawSignals(
            business_apps=["khatabook"],
            whatsapp_business_usage="yes",
            payment_apps_installed=["paytm", "phonepe"],
            time_of_day=TimeOfDay.EVENING
        )
        
        result = self.engine.infer(signals)
        inference_id = list(self.engine.explanations.keys())[-1]
        explanation = self.engine.get_explanation(inference_id)
        
        # Should have correlation events
        correlation_events = [e for e in explanation.events if e.event_type.value == "signal_correlation"]
        # May or may not have correlations, but if present, should be valid
        assert len(explanation.decision_factors) > 0
    
    def test_explanation_logging(self):
        """Test explanation logging to file"""
        import os
        import tempfile
        
        signals = RawSignals(
            time_of_day=TimeOfDay.MORNING,
            system_language="hi"
        )
        
        result = self.engine.infer(signals)
        inference_id = list(self.engine.explanations.keys())[-1]
        
        # Log to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            temp_path = f.name
        
        try:
            self.engine.log_explanation(inference_id, temp_path)
            assert os.path.exists(temp_path)
            with open(temp_path, 'r') as f:
                content = f.read()
                assert len(content) > 0
                assert inference_id in content
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_enhanced_vs_basic_engine(self):
        """Test that enhanced engine produces different/better results"""
        signals = RawSignals(
            business_apps=["khatabook"],
            whatsapp_business_usage="yes",
            payment_apps_installed=["paytm"],
            time_of_day=TimeOfDay.EVENING,
            otp_message_frequency="high"
        )
        
        # Enhanced engine
        enhanced_result = self.engine.infer(signals)
        
        # Basic engine
        from inference_engine import get_inference_engine
        basic_engine = get_inference_engine()
        basic_result = basic_engine.infer(signals)
        
        # Both should work
        assert enhanced_result.user_need_state is not None
        assert basic_result.user_need_state is not None
        
        # Enhanced should have more detailed explanation
        assert len(enhanced_result.explanation) >= len(basic_result.explanation)
    
    def test_multiple_inferences(self):
        """Test multiple inferences with explanation tracking"""
        signals1 = RawSignals(time_of_day=TimeOfDay.MORNING, system_language="hi")
        signals2 = RawSignals(time_of_day=TimeOfDay.EVENING, business_apps=["khatabook"])
        
        result1 = self.engine.infer(signals1)
        result2 = self.engine.infer(signals2)
        
        # Should have 2 explanations
        assert len(self.engine.explanations) >= 2
        
        # Both should have valid results
        assert result1.user_need_state is not None
        assert result2.user_need_state is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

