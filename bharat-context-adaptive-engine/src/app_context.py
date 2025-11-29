"""
App Context Module
Provides ChatGPT-specific context and understanding
"""

from typing import Dict, List, Any, Optional
from .models import RawSignals


class AppContext:
    """ChatGPT app-specific context and insights"""
    
    # ChatGPT-specific user behaviors and patterns
    CHATGPT_CONTEXT = {
        "first_time_user": {
            "indicators": ["first_prompt_attempted", "tutorial_started", "example_prompts_viewed"],
            "needs": ["onboarding", "example_prompts", "guidance"],
            "ui_mode": "standard",
            "language": "system_default"
        },
        "voice_preference": {
            "indicators": ["first_action", "voice_button_tapped", "microphone_permission"],
            "needs": ["voice_input", "voice_examples", "voice_guidance"],
            "ui_mode": "voice-first",
            "language": "system_default"
        },
        "low_engagement": {
            "indicators": ["session_duration", "text_input_length", "abandonment_indicators"],
            "needs": ["quick_wins", "simple_prompts", "immediate_value"],
            "ui_mode": "lite",
            "language": "system_default"
        },
        "high_engagement": {
            "indicators": ["session_duration", "return_user", "text_input_length"],
            "needs": ["advanced_features", "complex_prompts", "rich_experience"],
            "ui_mode": "standard",
            "language": "system_default"
        }
    }
    
    # ChatGPT use cases in Indian context
    INDIAN_USE_CASES = {
        "devotional": {
            "signals": ["time_of_day", "system_language", "first_action"],
            "prompts": ["bhajans", "prayers", "religious_quotes", "festival_messages"],
            "language": "hindi",
            "time": "morning"
        },
        "business_accounting": {
            "signals": ["business_apps", "payment_apps_installed", "time_of_day"],
            "prompts": ["calculations", "ledger_entries", "gst_calculations", "invoice_generation"],
            "language": "hindi",
            "time": "evening"
        },
        "student_help": {
            "signals": ["education_apps", "session_duration", "text_input_length"],
            "prompts": ["homework_help", "essay_writing", "subject_explanations", "exam_prep"],
            "language": "mixed",
            "time": "afternoon"
        },
        "shopping_assistance": {
            "signals": ["ecommerce_apps", "ecommerce_notifications", "shopping_app_count"],
            "prompts": ["product_comparisons", "price_checks", "shopping_lists", "reviews"],
            "language": "system_default",
            "time": "any"
        },
        "language_translation": {
            "signals": ["system_language", "keyboard_language", "messaging_language"],
            "prompts": ["translations", "language_learning", "text_conversion"],
            "language": "regional",
            "time": "any"
        }
    }
    
    def analyze_app_context(self, signals: RawSignals) -> Dict[str, Any]:
        """
        Analyze signals in context of ChatGPT app
        Returns app-specific insights
        """
        insights = []
        detected_use_cases = []
        ui_recommendations = {}
        prompt_suggestions = []
        
        # Analyze ChatGPT-specific behaviors
        chatgpt_insights = self._analyze_chatgpt_behaviors(signals)
        insights.extend(chatgpt_insights.get("insights", []))
        
        # Detect Indian use cases
        use_case_analysis = self._detect_indian_use_cases(signals)
        detected_use_cases.extend(use_case_analysis.get("use_cases", []))
        prompt_suggestions.extend(use_case_analysis.get("prompt_suggestions", []))
        
        # UI recommendations based on app context
        ui_recommendations = self._generate_ui_recommendations(signals)
        
        # Language recommendations
        language_recommendations = self._generate_language_recommendations(signals)
        
        return {
            "insights": insights,
            "detected_use_cases": detected_use_cases,
            "prompt_suggestions": prompt_suggestions,
            "ui_recommendations": ui_recommendations,
            "language_recommendations": language_recommendations,
            "app_context_applied": True
        }
    
    def _analyze_chatgpt_behaviors(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze ChatGPT-specific user behaviors"""
        insights = []
        
        # First-time user detection
        if (signals.first_prompt_attempted == "no" and 
            (signals.tutorial_started == "yes" or signals.example_prompts_viewed == "yes")):
            insights.append("First-time ChatGPT user - needs onboarding and guidance")
        
        # Voice preference
        if (signals.first_action == "voice" or 
            (signals.voice_button_tapped == "yes" and signals.microphone_permission == "granted")):
            insights.append("User prefers voice input - enable voice-first experience")
        
        # Low engagement
        if (signals.session_duration == "short" and 
            signals.text_input_length == "none" and
            signals.abandonment_indicators):
            insights.append("Low engagement detected - needs quick wins and simple prompts")
        
        # High engagement
        if (signals.session_duration == "long" and 
            signals.return_user == "yes" and
            signals.text_input_length == "long"):
            insights.append("High engagement - user ready for advanced features")
        
        return {"insights": insights}
    
    def _detect_indian_use_cases(self, signals: RawSignals) -> Dict[str, Any]:
        """Detect Indian-specific ChatGPT use cases"""
        use_cases = []
        prompt_suggestions = []
        
        # Devotional use case
        if (signals.time_of_day and signals.time_of_day.value in ["early_morning", "morning"] and
            signals.system_language == "hi" and
            signals.first_action == "voice"):
            use_cases.append("devotional")
            prompt_suggestions.extend([
                "Show devotional prompts (Bhajans, prayers)",
                "Enable voice input for morning prayers",
                "Display festival-specific content"
            ])
        
        # Business accounting use case
        if (signals.business_apps and isinstance(signals.business_apps, list) and len(signals.business_apps) > 0 and
            signals.payment_apps_installed and
            signals.time_of_day and signals.time_of_day.value == "evening"):
            use_cases.append("business_accounting")
            prompt_suggestions.extend([
                "Show calculation and ledger prompts",
                "Suggest GST calculation helpers",
                "Display invoice generation templates"
            ])
        
        # Student help use case
        if (signals.education_apps and isinstance(signals.education_apps, list) and len(signals.education_apps) > 0 and
            signals.session_duration == "long" and
            signals.text_input_length == "long"):
            use_cases.append("student_help")
            prompt_suggestions.extend([
                "Show study and exam preparation prompts",
                "Suggest subject-specific help",
                "Display essay writing helpers"
            ])
        
        # Shopping assistance use case
        if (signals.ecommerce_apps and isinstance(signals.ecommerce_apps, list) and len(signals.ecommerce_apps) > 0 and
            signals.ecommerce_notifications == "high"):
            use_cases.append("shopping_assistance")
            prompt_suggestions.extend([
                "Show product comparison prompts",
                "Suggest price check helpers",
                "Display shopping list templates"
            ])
        
        # Language translation use case
        if (signals.system_language and signals.system_language not in ["hi", "en"] and
            signals.keyboard_language and signals.keyboard_language != signals.system_language):
            use_cases.append("language_translation")
            prompt_suggestions.extend([
                "Show translation prompts",
                "Suggest language learning helpers",
                "Display text conversion tools"
            ])
        
        return {"use_cases": use_cases, "prompt_suggestions": prompt_suggestions}
    
    def _generate_ui_recommendations(self, signals: RawSignals) -> Dict[str, Any]:
        """Generate UI recommendations based on app context"""
        recommendations = {
            "ui_mode": "standard",
            "features": [],
            "optimizations": []
        }
        
        # Voice-first recommendation
        if signals.first_action == "voice" or signals.voice_button_tapped == "yes":
            recommendations["ui_mode"] = "voice-first"
            recommendations["features"].append("large_voice_button")
            recommendations["features"].append("voice_examples")
        
        # Lite mode recommendation
        if (signals.device_class and signals.device_class.value == "low_end" and
            signals.network_type and signals.network_type.value in ["2g", "3g"]):
            recommendations["ui_mode"] = "lite"
            recommendations["optimizations"].append("minimal_ui")
            recommendations["optimizations"].append("reduced_assets")
        
        # Standard mode with rich features
        if (signals.device_class and signals.device_class.value == "high_end" and
            signals.network_type and signals.network_type.value in ["wifi", "4g"]):
            recommendations["ui_mode"] = "standard"
            recommendations["features"].append("rich_formatting")
            recommendations["features"].append("advanced_prompts")
        
        return recommendations
    
    def _generate_language_recommendations(self, signals: RawSignals) -> Dict[str, Any]:
        """Generate language recommendations"""
        recommendations = {
            "primary_language": "system_default",
            "secondary_languages": [],
            "input_method": "keyboard"
        }
        
        # Hindi preference
        if signals.system_language == "hi":
            recommendations["primary_language"] = "hindi"
            if signals.messaging_language == "hindi" or signals.sms_language_mix == "hindi_only":
                recommendations["secondary_languages"] = ["english"]
        
        # Regional language preference
        if signals.system_language and signals.system_language not in ["hi", "en"]:
            recommendations["primary_language"] = "regional"
            recommendations["secondary_languages"] = ["hindi", "english"]
        
        # Voice input recommendation
        if signals.first_action == "voice" or signals.voice_button_tapped == "yes":
            recommendations["input_method"] = "voice"
        
        return recommendations

