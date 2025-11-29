"""
Web Intelligence Module
Provides contextual knowledge about signals based on web intelligence and research
"""

from typing import Dict, List, Any, Optional
from .models import RawSignals
from .llm_service import get_llm_service


class WebIntelligence:
    """Web intelligence and contextual knowledge about signals"""
    
    # Knowledge base about signal patterns and their meanings
    SIGNAL_PATTERNS = {
        # App Ecosystem Patterns
        "business_apps_present": {
            "meaning": "User likely runs a small business or shop",
            "context": "Apps like Khatabook, OkCredit indicate small business operations",
            "confidence_boost": 0.5,
            "related_signals": ["payment_apps_installed", "whatsapp_business_usage"]
        },
        "education_apps_present": {
            "meaning": "User is likely a student or parent of student",
            "context": "Education apps indicate learning-focused user",
            "confidence_boost": 0.4,
            "related_signals": ["session_duration", "text_input_length"]
        },
        "financial_apps_diverse": {
            "meaning": "User is financially active and tech-savvy",
            "context": "Multiple financial apps indicate active financial management",
            "confidence_boost": 0.3,
            "related_signals": ["banking_apps", "investment_apps"]
        },
        
        # SMS Patterns
        "high_otp_frequency": {
            "meaning": "User is actively transacting (payments, logins, verifications)",
            "context": "High OTP frequency indicates frequent digital transactions",
            "confidence_boost": 0.6,
            "related_signals": ["banking_sms_presence", "ecommerce_sms_presence", "payment_apps_installed"]
        },
        "banking_sms_present": {
            "meaning": "User has active banking relationship",
            "context": "Banking SMS indicates financial activity and trust in digital banking",
            "confidence_boost": 0.4,
            "related_signals": ["banking_apps", "upi_apps"]
        },
        "business_hours_sms": {
            "meaning": "User likely engaged in business activities during work hours",
            "context": "SMS during business hours suggests professional/business use",
            "confidence_boost": 0.3,
            "related_signals": ["business_apps", "whatsapp_business_usage"]
        },
        
        # WhatsApp Patterns
        "whatsapp_business_usage": {
            "meaning": "User uses WhatsApp for business communication",
            "context": "WhatsApp Business usage is common among small businesses in India",
            "confidence_boost": 0.7,
            "related_signals": ["business_apps", "payment_apps_installed", "business_hours_sms"]
        },
        "whatsapp_group_activity_high": {
            "meaning": "User is socially active, likely part of communities/families",
            "context": "High group activity indicates social engagement",
            "confidence_boost": 0.3,
            "related_signals": ["social_media_apps", "communication_apps"]
        },
        "whatsapp_notification_frequency_high": {
            "meaning": "User is highly engaged with messaging",
            "context": "High notification frequency indicates active communication",
            "confidence_boost": 0.2,
            "related_signals": ["total_notification_volume", "notification_response_rate"]
        },
        
        # Notification Patterns
        "high_notification_response_rate": {
            "meaning": "User is highly engaged and responsive",
            "context": "High response rate indicates active user who values notifications",
            "confidence_boost": 0.3,
            "related_signals": ["immediate_open_rate", "notification_to_app_launch"]
        },
        "ecommerce_notifications_high": {
            "meaning": "User is active online shopper",
            "context": "High e-commerce notifications indicate shopping activity",
            "confidence_boost": 0.4,
            "related_signals": ["ecommerce_apps", "shopping_app_count"]
        },
        
        # Device & Network Patterns
        "low_end_device_slow_network": {
            "meaning": "User has resource constraints, needs lite experience",
            "context": "Low-end device + slow network requires optimized experience",
            "confidence_boost": 0.5,
            "related_signals": ["device_class", "network_type", "network_speed"]
        },
        "high_end_device_fast_network": {
            "meaning": "User has premium device, can handle rich experiences",
            "context": "High-end device + fast network enables advanced features",
            "confidence_boost": 0.3,
            "related_signals": ["device_class", "network_type", "ram_size"]
        },
        
        # Language Patterns
        "hindi_dominant_signals": {
            "meaning": "User prefers Hindi language interface",
            "context": "Hindi is dominant language in North India, indicates regional preference",
            "confidence_boost": 0.4,
            "related_signals": ["system_language", "sms_language_mix", "messaging_language"]
        },
        "regional_language_signals": {
            "meaning": "User from non-Hindi speaking region",
            "context": "Regional language preference indicates cultural context",
            "confidence_boost": 0.4,
            "related_signals": ["system_language", "state", "language_region"]
        },
        
        # Temporal Patterns
        "morning_activity_pattern": {
            "meaning": "User active in morning, likely routine-based",
            "context": "Morning activity often indicates devotional or work routines",
            "confidence_boost": 0.3,
            "related_signals": ["time_of_day", "hour_of_day", "whatsapp_notification_time_distribution"]
        },
        "evening_activity_pattern": {
            "meaning": "User active in evening, likely work/business related",
            "context": "Evening activity often indicates business accounting or family time",
            "confidence_boost": 0.3,
            "related_signals": ["time_of_day", "hour_of_day", "business_hours_sms"]
        }
    }
    
    # Cultural and Regional Knowledge
    REGIONAL_PATTERNS = {
        "UP": {"primary_language": "hindi", "business_culture": "strong", "digital_adoption": "medium"},
        "MH": {"primary_language": "marathi", "business_culture": "strong", "digital_adoption": "high"},
        "GJ": {"primary_language": "gujarati", "business_culture": "very_strong", "digital_adoption": "high"},
        "TN": {"primary_language": "tamil", "business_culture": "strong", "digital_adoption": "high"},
        "KA": {"primary_language": "kannada", "business_culture": "strong", "digital_adoption": "high"},
        "WB": {"primary_language": "bengali", "business_culture": "medium", "digital_adoption": "medium"},
    }
    
    def __init__(self):
        self.llm_service = get_llm_service()

    # App Ecosystem Knowledge
    APP_ECOSYSTEM_INSIGHTS = {
        "khatabook": {
            "category": "business",
            "user_type": "small_business_owner",
            "typical_usage": "evening_accounting",
            "related_apps": ["okcredit", "bharatpe", "paytm"]
        },
        "byjus": {
            "category": "education",
            "user_type": "student_or_parent",
            "typical_usage": "afternoon_study",
            "related_apps": ["unacademy", "vedantu"]
        },
        "paytm": {
            "category": "payment",
            "user_type": "digitally_active",
            "typical_usage": "frequent_transactions",
            "related_apps": ["phonepe", "gpay", "bhim"]
        }
    }
    
    def analyze_signals(self, signals: RawSignals, use_perplexity: bool = False) -> Dict[str, Any]:
        """
        Analyze signals using web intelligence and contextual knowledge
        Returns insights and confidence adjustments
        """
        insights = []
        confidence_adjustments = {}
        detected_patterns = []
        
        # Analyze app ecosystem
        app_insights = self._analyze_app_ecosystem(signals)
        insights.extend(app_insights.get("insights", []))
        detected_patterns.extend(app_insights.get("patterns", []))
        
        # Analyze SMS patterns
        sms_insights = self._analyze_sms_patterns(signals)
        insights.extend(sms_insights.get("insights", []))
        detected_patterns.extend(sms_insights.get("patterns", []))
        
        # Analyze WhatsApp patterns
        whatsapp_insights = self._analyze_whatsapp_patterns(signals)
        insights.extend(whatsapp_insights.get("insights", []))
        detected_patterns.extend(whatsapp_insights.get("patterns", []))
        
        # Analyze notification patterns
        notification_insights = self._analyze_notification_patterns(signals)
        insights.extend(notification_insights.get("insights", []))
        detected_patterns.extend(notification_insights.get("patterns", []))
        
        # Analyze device/network patterns
        device_insights = self._analyze_device_network_patterns(signals)
        insights.extend(device_insights.get("insights", []))
        detected_patterns.extend(device_insights.get("patterns", []))
        
        # Analyze language patterns
        language_insights = self._analyze_language_patterns(signals)
        insights.extend(language_insights.get("insights", []))
        detected_patterns.extend(language_insights.get("patterns", []))
        
        # Analyze temporal patterns
        temporal_insights = self._analyze_temporal_patterns(signals)
        insights.extend(temporal_insights.get("insights", []))
        detected_patterns.extend(temporal_insights.get("patterns", []))
        
        # Calculate confidence adjustments
        for pattern in detected_patterns:
            if pattern in self.SIGNAL_PATTERNS:
                pattern_info = self.SIGNAL_PATTERNS[pattern]
                confidence_adjustments[pattern] = pattern_info.get("confidence_boost", 0.0)
        
        # Perplexity Integration for deeper context
        web_context = None
        if use_perplexity and detected_patterns:
            # Construct a query based on detected patterns
            patterns_str = ", ".join(detected_patterns[:3])
            query = f"What are the typical digital behaviors and needs of an Indian user showing these patterns: {patterns_str}?"
            web_context = self.llm_service.get_web_intelligence(query)
            if web_context:
                insights.append(f"Web Intelligence: {web_context[:200]}...")

        return {
            "insights": insights,
            "detected_patterns": detected_patterns,
            "confidence_adjustments": confidence_adjustments,
            "web_intelligence_applied": True,
            "web_context": web_context
        }
    
    def _analyze_app_ecosystem(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze installed app ecosystem"""
        insights = []
        patterns = []
        
        # Business apps
        if signals.business_apps and isinstance(signals.business_apps, list) and len(signals.business_apps) > 0:
            insights.append("Business apps detected - user likely runs small business")
            patterns.append("business_apps_present")
        
        # Education apps
        if signals.education_apps and isinstance(signals.education_apps, list) and len(signals.education_apps) > 0:
            insights.append("Education apps detected - user likely student or parent")
            patterns.append("education_apps_present")
        
        # Financial apps diversity
        financial_count = 0
        if signals.payment_apps_installed:
            financial_count += 1
        if signals.banking_apps == "yes":
            financial_count += 1
        if signals.investment_apps and isinstance(signals.investment_apps, list):
            financial_count += len(signals.investment_apps)
        
        if financial_count >= 3:
            insights.append("Diverse financial app ecosystem - user is financially active")
            patterns.append("financial_apps_diverse")
        
        return {"insights": insights, "patterns": patterns}
    
    def _analyze_sms_patterns(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze SMS patterns"""
        insights = []
        patterns = []
        
        if signals.otp_message_frequency == "high":
            insights.append("High OTP frequency - user actively transacting")
            patterns.append("high_otp_frequency")
        
        if signals.banking_sms_presence == "yes":
            insights.append("Banking SMS present - active banking relationship")
            patterns.append("banking_sms_present")
        
        if signals.business_hours_sms == "yes":
            insights.append("Business hours SMS activity - likely business user")
            patterns.append("business_hours_sms")
        
        return {"insights": insights, "patterns": patterns}
    
    def _analyze_whatsapp_patterns(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze WhatsApp patterns"""
        insights = []
        patterns = []
        
        if signals.whatsapp_business_usage == "yes":
            insights.append("WhatsApp Business usage - small business owner")
            patterns.append("whatsapp_business_usage")
        
        if signals.whatsapp_group_activity == "high":
            insights.append("High WhatsApp group activity - socially engaged")
            patterns.append("whatsapp_group_activity_high")
        
        if signals.whatsapp_notification_frequency == "high":
            insights.append("High WhatsApp notification frequency - active communicator")
            patterns.append("whatsapp_notification_frequency_high")
        
        return {"insights": insights, "patterns": patterns}
    
    def _analyze_notification_patterns(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze notification patterns"""
        insights = []
        patterns = []
        
        if signals.notification_response_rate == "high":
            insights.append("High notification response rate - engaged user")
            patterns.append("high_notification_response_rate")
        
        if signals.ecommerce_notifications == "high":
            insights.append("High e-commerce notifications - active shopper")
            patterns.append("ecommerce_notifications_high")
        
        return {"insights": insights, "patterns": patterns}
    
    def _analyze_device_network_patterns(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze device and network patterns"""
        insights = []
        patterns = []
        
        if (signals.device_class and signals.device_class.value == "low_end" and 
            signals.network_type and signals.network_type.value in ["2g", "3g"]):
            insights.append("Low-end device with slow network - needs lite experience")
            patterns.append("low_end_device_slow_network")
        
        if (signals.device_class and signals.device_class.value == "high_end" and
            signals.network_type and signals.network_type.value in ["wifi", "4g"]):
            insights.append("High-end device with fast network - can handle rich features")
            patterns.append("high_end_device_fast_network")
        
        return {"insights": insights, "patterns": patterns}
    
    def _analyze_language_patterns(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze language patterns"""
        insights = []
        patterns = []
        
        if signals.system_language == "hi":
            if signals.sms_language_mix == "hindi_only" or signals.messaging_language == "hindi":
                insights.append("Hindi-dominant signals - North Indian user")
                patterns.append("hindi_dominant_signals")
        
        if signals.system_language and signals.system_language not in ["hi", "en"]:
            insights.append("Regional language preference - non-Hindi speaking region")
            patterns.append("regional_language_signals")
        
        return {"insights": insights, "patterns": patterns}
    
    def _analyze_temporal_patterns(self, signals: RawSignals) -> Dict[str, Any]:
        """Analyze temporal patterns"""
        insights = []
        patterns = []
        
        if signals.time_of_day and signals.time_of_day.value in ["early_morning", "morning"]:
            if signals.hour_of_day and 5 <= signals.hour_of_day <= 9:
                insights.append("Morning activity pattern - likely routine-based")
                patterns.append("morning_activity_pattern")
        
        if signals.time_of_day and signals.time_of_day.value == "evening":
            if signals.hour_of_day and 18 <= signals.hour_of_day <= 22:
                insights.append("Evening activity pattern - likely work/business related")
                patterns.append("evening_activity_pattern")
        
        return {"insights": insights, "patterns": patterns}

