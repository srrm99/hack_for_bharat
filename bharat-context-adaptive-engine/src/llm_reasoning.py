"""
LLM Reasoning Module
Uses worldly knowledge and LLM capabilities for advanced reasoning
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date
from .models import RawSignals
from .llm_service import get_llm_service
import json


class LLMReasoning:
    """LLM-based reasoning for inference"""
    
    def __init__(self):
        self.llm_service = get_llm_service()
    
    # Worldly knowledge patterns
    WORLD_KNOWLEDGE = {
        "indian_business_culture": {
            "insight": "Small businesses in India often use WhatsApp for customer communication and evening time for accounting",
            "applies_to": ["business_apps", "whatsapp_business_usage", "evening_activity"],
            "confidence_boost": 0.4
        },
        "indian_education_system": {
            "insight": "Indian students often use education apps in afternoon/evening for exam preparation",
            "applies_to": ["education_apps", "afternoon_activity", "long_sessions"],
            "confidence_boost": 0.3
        },
        "indian_digital_payment_adoption": {
            "insight": "High OTP frequency and multiple payment apps indicate active digital payment user in India",
            "applies_to": ["otp_frequency", "payment_apps", "banking_sms"],
            "confidence_boost": 0.5
        },
        "indian_language_preferences": {
            "insight": "Hindi-dominant users in North India prefer Hindi interface, regional language users prefer regional",
            "applies_to": ["system_language", "state", "messaging_language"],
            "confidence_boost": 0.4
        },
        "indian_festival_culture": {
            "insight": "Festival days see increased devotional and messaging activity",
            "applies_to": ["festival_day", "morning_activity", "whatsapp_notifications"],
            "confidence_boost": 0.3
        },
        "indian_device_constraints": {
            "insight": "Tier-2/3/4 users often have low-end devices and slow networks, need optimized experiences",
            "applies_to": ["device_class", "network_type", "city_tier"],
            "confidence_boost": 0.5
        },
        "indian_social_communication": {
            "insight": "WhatsApp is primary communication tool in India, high group activity indicates social engagement",
            "applies_to": ["whatsapp_installed", "whatsapp_group_activity", "notification_frequency"],
            "confidence_boost": 0.3
        }
    }
    
    def reason(self, signals: RawSignals, web_intelligence: Dict[str, Any], 
               app_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply LLM reasoning and worldly knowledge
        """
        insights = []
        reasoning_steps = []
        confidence_adjustments = {}
        llm_inference_result = {}
        
        # 1. Try Real LLM Inference (OpenRouter)
        try:
            # Helper for JSON serialization
            def json_serial(obj):
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                return str(obj)

            # Construct context from web intelligence and app context to help LLM
            context_str = f"Web Intelligence: {json.dumps(web_intelligence, default=json_serial)}\nApp Context: {json.dumps(app_context, default=json_serial)}"
            
            llm_output = self.llm_service.infer_user_profile_with_reasoning(signals, context_str)
            
            if "error" not in llm_output:
                llm_inference_result = llm_output
                insights.append(f"LLM Inference: Identified as {llm_output.get('user_need_state')}")
                reasoning_steps.append({
                    "step": "llm_inference",
                    "reasoning": llm_output.get("reasoning_summary", "LLM reasoning applied"),
                    "output": llm_output
                })
                # Add confidence from LLM
                # Mapping LLM confidence (0-10) to adjustment? Or use it directly later.
        except Exception as e:
            print(f"LLM Reasoning failed: {e}")
            # Fallback to static rules if LLM fails

        # 2. Apply worldly knowledge patterns (Static/Fallback)
        knowledge_insights = self._apply_worldly_knowledge(signals, web_intelligence, app_context)
        insights.extend(knowledge_insights.get("insights", []))
        reasoning_steps.extend(knowledge_insights.get("reasoning_steps", []))
        confidence_adjustments.update(knowledge_insights.get("confidence_adjustments", {}))
        
        # Cross-signal correlation reasoning
        correlation_insights = self._correlate_signals(signals, web_intelligence, app_context)
        insights.extend(correlation_insights.get("insights", []))
        reasoning_steps.extend(correlation_insights.get("reasoning_steps", []))
        
        # Contextual inference
        contextual_insights = self._contextual_inference(signals, web_intelligence, app_context)
        insights.extend(contextual_insights.get("insights", []))
        reasoning_steps.extend(contextual_insights.get("reasoning_steps", []))
        
        return {
            "insights": insights,
            "reasoning_steps": reasoning_steps,
            "confidence_adjustments": confidence_adjustments,
            "llm_reasoning_applied": True,
            "llm_inference_result": llm_inference_result # Return the structured LLM result
        }
    
    def _apply_worldly_knowledge(self, signals: RawSignals, web_intelligence: Dict[str, Any],
                                app_context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply worldly knowledge patterns"""
        insights = []
        reasoning_steps = []
        confidence_adjustments = {}
        
        # Indian business culture
        if (signals.business_apps and isinstance(signals.business_apps, list) and len(signals.business_apps) > 0 and
            signals.whatsapp_business_usage == "yes" and
            signals.time_of_day and signals.time_of_day.value == "evening"):
            insight = "Indian business culture: Small businesses use WhatsApp for customer communication and evening for accounting"
            insights.append(insight)
            reasoning_steps.append({
                "step": "worldly_knowledge",
                "pattern": "indian_business_culture",
                "reasoning": insight,
                "signals_used": ["business_apps", "whatsapp_business_usage", "time_of_day"]
            })
            confidence_adjustments["indian_business_culture"] = 0.4
        
        # Indian education system
        if (signals.education_apps and isinstance(signals.education_apps, list) and len(signals.education_apps) > 0 and
            signals.time_of_day and signals.time_of_day.value in ["afternoon", "evening"] and
            signals.session_duration == "long"):
            insight = "Indian education system: Students use education apps in afternoon/evening for exam prep"
            insights.append(insight)
            reasoning_steps.append({
                "step": "worldly_knowledge",
                "pattern": "indian_education_system",
                "reasoning": insight,
                "signals_used": ["education_apps", "time_of_day", "session_duration"]
            })
            confidence_adjustments["indian_education_system"] = 0.3
        
        # Indian digital payment adoption
        if (signals.otp_message_frequency == "high" and
            signals.payment_apps_installed and isinstance(signals.payment_apps_installed, list) and len(signals.payment_apps_installed) >= 2 and
            signals.banking_sms_presence == "yes"):
            insight = "Indian digital payment adoption: High OTP frequency + multiple payment apps = active digital payment user"
            insights.append(insight)
            reasoning_steps.append({
                "step": "worldly_knowledge",
                "pattern": "indian_digital_payment_adoption",
                "reasoning": insight,
                "signals_used": ["otp_message_frequency", "payment_apps_installed", "banking_sms_presence"]
            })
            confidence_adjustments["indian_digital_payment_adoption"] = 0.5
        
        # Indian language preferences
        if signals.system_language == "hi" and signals.state in ["UP", "MP", "BH", "RJ"]:
            insight = "Indian language preferences: Hindi-dominant users in North India prefer Hindi interface"
            insights.append(insight)
            reasoning_steps.append({
                "step": "worldly_knowledge",
                "pattern": "indian_language_preferences",
                "reasoning": insight,
                "signals_used": ["system_language", "state"]
            })
            confidence_adjustments["indian_language_preferences"] = 0.4
        
        # Indian device constraints
        if (signals.device_class and signals.device_class.value == "low_end" and
            signals.network_type and signals.network_type.value in ["2g", "3g"] and
            signals.city_tier in ["tier3", "tier4", "rural"]):
            insight = "Indian device constraints: Tier-2/3/4 users often have low-end devices and slow networks, need optimized experiences"
            insights.append(insight)
            reasoning_steps.append({
                "step": "worldly_knowledge",
                "pattern": "indian_device_constraints",
                "reasoning": insight,
                "signals_used": ["device_class", "network_type", "city_tier"]
            })
            confidence_adjustments["indian_device_constraints"] = 0.5
        
        # Indian social communication
        if (signals.whatsapp_installed == "yes" and
            signals.whatsapp_group_activity == "high" and
            signals.whatsapp_notification_frequency == "high"):
            insight = "Indian social communication: WhatsApp is primary communication tool, high group activity = social engagement"
            insights.append(insight)
            reasoning_steps.append({
                "step": "worldly_knowledge",
                "pattern": "indian_social_communication",
                "reasoning": insight,
                "signals_used": ["whatsapp_installed", "whatsapp_group_activity", "whatsapp_notification_frequency"]
            })
            confidence_adjustments["indian_social_communication"] = 0.3
        
        return {
            "insights": insights,
            "reasoning_steps": reasoning_steps,
            "confidence_adjustments": confidence_adjustments
        }
    
    def _correlate_signals(self, signals: RawSignals, web_intelligence: Dict[str, Any],
                          app_context: Dict[str, Any]) -> Dict[str, Any]:
        """Correlate multiple signals for deeper insights"""
        insights = []
        reasoning_steps = []
        
        # Business user correlation
        if (signals.business_apps and isinstance(signals.business_apps, list) and len(signals.business_apps) > 0 and
            signals.whatsapp_business_usage == "yes" and
            signals.payment_apps_installed and isinstance(signals.payment_apps_installed, list) and len(signals.payment_apps_installed) >= 2 and
            signals.time_of_day and signals.time_of_day.value == "evening"):
            insight = "Strong correlation: Business apps + WhatsApp Business + Payment apps + Evening = Shop Owner"
            insights.append(insight)
            reasoning_steps.append({
                "step": "signal_correlation",
                "correlation": "business_user_strong",
                "reasoning": "Multiple business-related signals converge to indicate shop owner",
                "signals_correlated": ["business_apps", "whatsapp_business_usage", "payment_apps_installed", "time_of_day"]
            })
        
        # Student correlation
        if (signals.education_apps and isinstance(signals.education_apps, list) and len(signals.education_apps) > 0 and
            signals.session_duration == "long" and
            signals.text_input_length == "long" and
            signals.total_notification_volume == "low"):
            insight = "Strong correlation: Education apps + Long sessions + Long text + Low notifications = Student"
            insights.append(insight)
            reasoning_steps.append({
                "step": "signal_correlation",
                "correlation": "student_strong",
                "reasoning": "Education-focused signals with low distractions indicate student",
                "signals_correlated": ["education_apps", "session_duration", "text_input_length", "total_notification_volume"]
            })
        
        return {"insights": insights, "reasoning_steps": reasoning_steps}
    
    def _contextual_inference(self, signals: RawSignals, web_intelligence: Dict[str, Any],
                             app_context: Dict[str, Any]) -> Dict[str, Any]:
        """Contextual inference combining all sources"""
        insights = []
        reasoning_steps = []
        
        # Combine web intelligence and app context
        if web_intelligence.get("detected_patterns") and app_context.get("detected_use_cases"):
            web_patterns = web_intelligence.get("detected_patterns", [])
            app_use_cases = app_context.get("detected_use_cases", [])
            
            # Business use case with web intelligence
            if "business_apps_present" in web_patterns and "business_accounting" in app_use_cases:
                insight = "Contextual inference: Web intelligence (business apps) + App context (accounting use case) = Evening Ledger User"
                insights.append(insight)
                reasoning_steps.append({
                    "step": "contextual_inference",
                    "inference": "evening_ledger_user",
                    "reasoning": "Combined web intelligence and app context confirm business accounting use case",
                    "sources": ["web_intelligence", "app_context"]
                })
            
            # Student use case with web intelligence
            if "education_apps_present" in web_patterns and "student_help" in app_use_cases:
                insight = "Contextual inference: Web intelligence (education apps) + App context (student help) = Student Exam User"
                insights.append(insight)
                reasoning_steps.append({
                    "step": "contextual_inference",
                    "inference": "student_exam_user",
                    "reasoning": "Combined web intelligence and app context confirm student use case",
                    "sources": ["web_intelligence", "app_context"]
                })
        
        return {"insights": insights, "reasoning_steps": reasoning_steps}

